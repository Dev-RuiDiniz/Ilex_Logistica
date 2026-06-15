"""Alerts generation service for BETA-017A / BETA-027."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert, AlertDeliveryLog
from app.modules.shipments.exceptions_service import classify_exception_type
from app.modules.shipments.models import Shipment
from app.modules.sla.service import calculate_shipment_sla
from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest

logger = logging.getLogger(__name__)

# Configuration constants
NO_UPDATE_DAYS_THRESHOLD = 7  # Days without update to trigger alert
IMPORT_FAILURE_MAX_AGE_HOURS = 24  # Max age of failed imports to alert on


def generate_alerts(db: Session) -> dict[str, Any]:
    """Generate alerts from SLA and exceptions data.

    This function is idempotent - it will not create duplicate alerts
    for the same source when an active alert already exists.

    Args:
        db: Database session

    Returns:
        Dictionary with generation results:
        - success: bool
        - processed_count: int
        - created_count: int
        - skipped_count: int
        - resolved_count: int
        - error_count: int
    """
    processed_count = 0
    created_count = 0
    skipped_count = 0
    resolved_count = 0
    error_count = 0

    try:
        # Get all active shipments
        shipments = db.query(Shipment).filter(Shipment.is_active.is_(True)).all()

        for shipment in shipments:
            processed_count += 1

            try:
                # Calculate SLA for this shipment
                sla_result = calculate_shipment_sla(db, shipment.id)
                sla_status = sla_result.get("sla_status")
                delay_days = sla_result.get("delay_days", 0)
                is_late = sla_result.get("is_late", False)

                # Classify exception type
                exc_type = classify_exception_type(sla_status, shipment.criticality, is_late)

                # Determine alert type and severity based on SLA status
                alert_type, severity, title, message = _determine_alert_details(
                    sla_status, exc_type, delay_days, shipment
                )

                if alert_type is None:
                    # No alert needed for this shipment
                    # Check if there's an active alert that should be resolved
                    _resolve_stale_alerts(db, shipment.id, alert_type)
                    continue

                # Check if alert already exists for this source
                existing_alert = db.query(Alert).filter(
                    Alert.source_type == "shipment",
                    Alert.source_id == shipment.id,
                    Alert.alert_type == alert_type,
                    Alert.status == "active",
                    Alert.is_resolved.is_(False)
                ).first()

                if existing_alert:
                    # Alert already exists, skip
                    skipped_count += 1
                    continue

                # Create new alert
                alert = Alert(
                    alert_type=alert_type,
                    severity=severity,
                    title=title,
                    message=message,
                    source_type="shipment",
                    source_id=shipment.id,
                    shipment_id=shipment.id,
                    carrier_id=shipment.carrier_id,
                    status="active",
                    is_read=False,
                    is_resolved=False,
                    generated_at=datetime.now(UTC),
                )
                db.add(alert)
                created_count += 1

            except Exception as e:
                error_count += 1
                continue

        db.commit()
        
        # Audit log
        try:
            audit_log = AuditLogCreateRequest(
                event_type="alert_generated",
                entity_type="alert",
                action="create",
                source="system",
                severity="info",
                status="success",
                message=f"Alertas gerados: {created_count} criados",
                metadata_json=f'{{"created_count": {created_count}}}',
            )
            AuditLogService.create_log(db, audit_log)
        except Exception as e:
            logger.error(f"Failed to create audit log for alerts: {e}")

        return {
            "success": True,
            "processed_count": processed_count,
            "created_count": created_count,
            "skipped_count": skipped_count,
            "resolved_count": resolved_count,
            "error_count": error_count,
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "processed_count": processed_count,
            "created_count": created_count,
            "skipped_count": skipped_count,
            "resolved_count": resolved_count,
            "error_count": error_count + 1,
        }


def _determine_alert_details(
    sla_status: str | None,
    exc_type: str | None,
    delay_days: int,
    shipment: Shipment,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Determine alert type, severity, title and message.

    Args:
        sla_status: SLA status
        exc_type: Exception type
        delay_days: Delay days
        shipment: Shipment object

    Returns:
        Tuple of (alert_type, severity, title, message) or (None, None, None, None)
    """
    if sla_status == "critical" or exc_type == "critical":
        return (
            "sla_critical",
            "critical",
            "Atraso Crítico",
            f"Entrega {shipment.tracking_code} com atraso crítico de {delay_days} dias",
        )
    elif sla_status == "late" or exc_type == "late":
        return (
            "sla_late",
            "warning",
            "Atraso",
            f"Entrega {shipment.tracking_code} atrasada em {delay_days} dias",
        )
    elif sla_status == "warning" or exc_type == "warning":
        return (
            "sla_warning",
            "info",
            "Atenção",
            f"Entrega {shipment.tracking_code} próxima ao prazo",
        )
    elif sla_status == "unknown" or exc_type == "unknown_sla":
        return (
            "unknown_sla",
            "info",
            "SLA Desconhecido",
            f"Entrega {shipment.tracking_code} sem SLA definido",
        )

    return None, None, None, None


def _resolve_stale_alerts(db: Session, shipment_id: int, alert_type: str | None) -> None:
    """Resolve stale alerts for a shipment.

    Args:
        db: Database session
        shipment_id: Shipment ID
        alert_type: Alert type to resolve (None resolves all)
    """
    query = db.query(Alert).filter(
        Alert.source_type == "shipment",
        Alert.source_id == shipment_id,
        Alert.status == "active",
        Alert.is_resolved.is_(False)
    )

    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)

    alerts = query.all()

    for alert in alerts:
        alert.status = "resolved"
        alert.is_resolved = True
        alert.resolved_at = datetime.now(UTC)


def get_active_alerts_count(db: Session) -> int:
    """Get count of active alerts.

    Args:
        db: Database session

    Returns:
        Count of active alerts
    """
    return db.query(Alert).filter(
        Alert.status == "active",
        Alert.is_resolved.is_(False)
    ).count()


def generate_no_update_alerts(db: Session) -> dict[str, int]:
    """Generate alerts for shipments without updates for X days.

    Args:
        db: Database session

    Returns:
        Dictionary with created_count and skipped_count
    """
    created_count = 0
    skipped_count = 0

    cutoff_date = datetime.now(UTC) - timedelta(days=NO_UPDATE_DAYS_THRESHOLD)

    # Find active shipments not updated in threshold days
    shipments = db.query(Shipment).filter(
        Shipment.is_active.is_(True),
        Shipment.updated_at < cutoff_date
    ).all()

    for shipment in shipments:
        # Check if alert already exists
        existing_alert = db.query(Alert).filter(
            Alert.source_type == "shipment",
            Alert.source_id == shipment.id,
            Alert.alert_type == "no_update",
            Alert.status == "active",
            Alert.is_resolved.is_(False)
        ).first()

        if existing_alert:
            skipped_count += 1
            continue

        alert = Alert(
            alert_type="no_update",
            severity="warning",
            title="Sem Atualização",
            message=f"Entrega {shipment.tracking_code} sem atualização há {NO_UPDATE_DAYS_THRESHOLD} dias",
            source_type="shipment",
            source_id=shipment.id,
            shipment_id=shipment.id,
            carrier_id=shipment.carrier_id,
            status="active",
            is_read=False,
            is_resolved=False,
            generated_at=datetime.now(UTC),
        )
        db.add(alert)
        created_count += 1

    db.commit()
    return {"created_count": created_count, "skipped_count": skipped_count}


def generate_import_failure_alerts(db: Session) -> dict[str, int]:
    """Generate alerts for failed imports.

    Args:
        db: Database session

    Returns:
        Dictionary with created_count and skipped_count
    """
    created_count = 0
    skipped_count = 0

    # Import here to avoid circular imports
    from app.modules.imports.models import ImportHistory

    cutoff_date = datetime.now(UTC) - timedelta(hours=IMPORT_FAILURE_MAX_AGE_HOURS)

    # Find failed imports within time window
    failed_imports = db.query(ImportHistory).filter(
        ImportHistory.status == "failed",
        ImportHistory.created_at >= cutoff_date
    ).all()

    for import_record in failed_imports:
        # Check if alert already exists
        existing_alert = db.query(Alert).filter(
            Alert.source_type == "import",
            Alert.source_id == import_record.id,
            Alert.alert_type == "import_failure",
            Alert.status == "active",
            Alert.is_resolved.is_(False)
        ).first()

        if existing_alert:
            skipped_count += 1
            continue

        error_msg = import_record.errors[0].message if import_record.errors else "Erro desconhecido"
        alert = Alert(
            alert_type="import_failure",
            severity="critical",
            title="Falha na Importação",
            message=f"Importação {import_record.filename} falhou: {error_msg}",
            source_type="import",
            source_id=import_record.id,
            status="active",
            is_read=False,
            is_resolved=False,
            generated_at=datetime.now(UTC),
        )
        db.add(alert)
        created_count += 1

    db.commit()
    return {"created_count": created_count, "skipped_count": skipped_count}


def create_delivery_log(
    db: Session,
    alert_id: int,
    channel: str,
    recipient: str,
    message: str,
    subject: str | None = None,
    max_attempts: int = 3
) -> AlertDeliveryLog:
    """Create a delivery log entry for an alert notification.

    Args:
        db: Database session
        alert_id: Alert ID
        channel: Delivery channel (email, sms, webhook, push)
        recipient: Recipient address
        message: Message content
        subject: Optional subject
        max_attempts: Maximum delivery attempts

    Returns:
        Created AlertDeliveryLog
    """
    log = AlertDeliveryLog(
        alert_id=alert_id,
        channel=channel,
        recipient=recipient,
        subject=subject,
        message=message,
        status="pending",
        attempts=0,
        max_attempts=max_attempts,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def update_delivery_log_status(
    db: Session,
    log_id: int,
    status: str,
    error_message: str | None = None,
    sent: bool = False
) -> AlertDeliveryLog | None:
    """Update delivery log status.

    Args:
        db: Database session
        log_id: Delivery log ID
        status: New status (pending, sent, failed)
        error_message: Optional error message
        sent: Whether the delivery was sent

    Returns:
        Updated AlertDeliveryLog or None if not found
    """
    log = db.query(AlertDeliveryLog).filter(AlertDeliveryLog.id == log_id).first()
    if not log:
        return None

    log.status = status
    log.error_message = error_message
    log.attempts += 1

    if sent:
        log.sent_at = datetime.now(UTC)

    db.commit()
    db.refresh(log)
    return log


def get_pending_delivery_logs(db: Session, max_attempts: int = 3) -> list[AlertDeliveryLog]:
    """Get pending delivery logs ready for retry.

    Args:
        db: Database session
        max_attempts: Maximum attempts before giving up

    Returns:
        List of pending AlertDeliveryLog
    """
    return db.query(AlertDeliveryLog).filter(
        AlertDeliveryLog.status.in_(["pending", "failed"]),
        AlertDeliveryLog.attempts < max_attempts
    ).all()
