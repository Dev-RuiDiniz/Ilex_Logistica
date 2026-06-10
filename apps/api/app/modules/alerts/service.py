"""Alerts generation service for BETA-017A."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert
from app.modules.shipments.exceptions_service import classify_exception_type
from app.modules.shipments.models import Shipment
from app.modules.sla.service import calculate_shipment_sla
from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest

logger = logging.getLogger(__name__)


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
