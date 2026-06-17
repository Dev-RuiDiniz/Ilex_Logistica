"""Alerts generation service for BETA-017A / BETA-027."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status as http_status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert, AlertDeliveryLog
from app.modules.audit.schemas import AuditLogCreateRequest
from app.modules.audit.service import AuditLogService
from app.modules.imports.models import ImportHistory
from app.modules.shipments.exceptions_service import classify_exception_type
from app.modules.shipments.models import Shipment
from app.modules.sla.service import calculate_shipment_sla

logger = logging.getLogger(__name__)

NO_UPDATE_ALERT_DAYS = 7
FINAL_SHIPMENT_STATUSES = {"delivered", "cancelled", "canceled"}


def _normalize_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _is_no_update_shipment(shipment: Shipment, *, now: datetime | None = None) -> tuple[bool, int]:
    """Return whether a shipment is stale enough to trigger a no-update alert."""
    updated_at = _normalize_datetime(shipment.updated_at)
    if updated_at is None:
        return False, 0

    shipment_status = (shipment.status or "").lower()
    if shipment_status in FINAL_SHIPMENT_STATUSES:
        return False, 0

    reference_now = now or datetime.now(UTC)
    delta = reference_now - updated_at
    if delta >= timedelta(days=NO_UPDATE_ALERT_DAYS):
        stale_days = max(delta.days, NO_UPDATE_ALERT_DAYS)
        return True, stale_days
    return False, 0


def _build_shipment_alert_details(
    shipment: Shipment,
    sla_status: str | None,
    exception_type: str | None,
    delay_days: int,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Determine the alert payload for a shipment."""
    if sla_status == "critical" or exception_type == "critical":
        return (
            "sla_critical",
            "critical",
            "Atraso Crítico",
            f"Entrega {shipment.tracking_code} com atraso crítico de {delay_days} dias",
        )
    if sla_status == "late" or exception_type == "late":
        return (
            "sla_late",
            "warning",
            "Atraso",
            f"Entrega {shipment.tracking_code} atrasada em {delay_days} dias",
        )
    if sla_status == "warning" or exception_type == "warning":
        return (
            "sla_warning",
            "info",
            "Atenção",
            f"Entrega {shipment.tracking_code} próxima ao prazo",
        )
    if sla_status == "unknown" or exception_type == "unknown_sla":
        return (
            "unknown_sla",
            "info",
            "SLA Desconhecido",
            f"Entrega {shipment.tracking_code} sem SLA definido",
        )

    is_stale, stale_days = _is_no_update_shipment(shipment)
    if is_stale:
        return (
            "no_update",
            "warning",
            "Sem Atualização",
            f"Entrega {shipment.tracking_code} sem atualização há {stale_days} dias",
        )

    return None, None, None, None


def _build_import_failure_alert_details(history: ImportHistory) -> tuple[str, str, str, str]:
    rejected_rows = max(history.rejected_count, history.rows_received - history.imported_count)
    title = "Falha de Importação"
    message = (
        f"Importação {history.filename} falhou com {rejected_rows} linha(s) rejeitada(s)"
        if rejected_rows
        else f"Importação {history.filename} falhou"
    )
    return "import_failure", "critical", title, message


def _create_delivery_log(
    db: Session,
    *,
    event_type: str,
    source_type: str,
    source_id: int | None,
    alert_type: str | None,
    alert: Alert | None = None,
    delivery_status: str = "success",
    message: str | None = None,
    metadata_json: str | None = None,
) -> AlertDeliveryLog:
    log_entry = AlertDeliveryLog(
        alert_id=alert.id if alert else None,
        event_type=event_type,
        delivery_channel="in_app",
        delivery_status=delivery_status,
        source_type=source_type,
        source_id=source_id,
        alert_type=alert_type,
        message=message,
        metadata_json=metadata_json,
    )
    db.add(log_entry)
    return log_entry


def _resolve_alerts(
    db: Session,
    alerts: list[Alert],
    *,
    event_type: str,
) -> int:
    resolved_count = 0
    for alert in alerts:
        if alert.is_resolved and alert.status == "resolved":
            continue
        alert.status = "resolved"
        alert.is_resolved = True
        alert.resolved_at = datetime.now(UTC)
        resolved_count += 1
        _create_delivery_log(
            db,
            event_type=event_type,
            source_type=alert.source_type,
            source_id=alert.source_id,
            alert_type=alert.alert_type,
            alert=alert,
            delivery_status="resolved",
            message=f"Alerta {alert.id} resolvido automaticamente",
        )
    return resolved_count


def _sync_active_alert_for_source(
    db: Session,
    *,
    source_type: str,
    source_id: int,
    alert_type: str | None,
    severity: str | None,
    title: str | None,
    message: str | None,
    shipment_id: int | None = None,
    carrier_id: int | None = None,
) -> tuple[int, int, int]:
    """Create or update a single active alert per source.

    Returns a tuple of (created_count, skipped_count, resolved_count).
    """
    active_alerts = (
        db.query(Alert)
        .filter(
            Alert.source_type == source_type,
            Alert.source_id == source_id,
            Alert.status == "active",
            Alert.is_resolved.is_(False),
        )
        .order_by(Alert.generated_at.desc())
        .all()
    )

    if alert_type is None:
        return 0, 0, _resolve_alerts(db, active_alerts, event_type="auto_resolved")

    matching_alert = next((alert for alert in active_alerts if alert.alert_type == alert_type), None)
    if matching_alert:
        stale_alerts = [alert for alert in active_alerts if alert.id != matching_alert.id]
        resolved_count = _resolve_alerts(db, stale_alerts, event_type="auto_resolved")
        _create_delivery_log(
            db,
            event_type="skipped_duplicate",
            source_type=source_type,
            source_id=source_id,
            alert_type=alert_type,
            alert=matching_alert,
            delivery_status="skipped",
            message="Alerta ativo já existente para a mesma origem",
        )
        return 0, 1, resolved_count

    resolved_count = _resolve_alerts(db, active_alerts, event_type="auto_resolved")

    alert = Alert(
        alert_type=alert_type,
        severity=severity or "info",
        title=title or "Alerta",
        message=message or "Alerta gerado automaticamente",
        source_type=source_type,
        source_id=source_id,
        shipment_id=shipment_id,
        carrier_id=carrier_id,
        status="active",
        is_read=False,
        is_resolved=False,
        generated_at=datetime.now(UTC),
    )
    db.add(alert)
    db.flush()
    _create_delivery_log(
        db,
        event_type="generated",
        source_type=source_type,
        source_id=source_id,
        alert_type=alert_type,
        alert=alert,
        delivery_status="success",
        message=message,
    )
    return 1, 0, resolved_count


def _sync_shipment_alert(db: Session, shipment: Shipment) -> tuple[int, int, int]:
    sla_result = calculate_shipment_sla(db, shipment.id)
    sla_status = sla_result.get("sla_status")
    delay_days = sla_result.get("delay_days", 0)
    is_late = sla_result.get("is_late", False)
    exception_type = classify_exception_type(sla_status, shipment.criticality, is_late)

    alert_type, severity, title, message = _build_shipment_alert_details(
        shipment,
        sla_status,
        exception_type,
        delay_days,
    )
    return _sync_active_alert_for_source(
        db,
        source_type="shipment",
        source_id=shipment.id,
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        shipment_id=shipment.id,
        carrier_id=shipment.carrier_id,
    )


def _sync_import_failure_alert(db: Session, history: ImportHistory) -> tuple[int, int, int]:
    alert_type, severity, title, message = _build_import_failure_alert_details(history)
    return _sync_active_alert_for_source(
        db,
        source_type="import",
        source_id=history.id,
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
    )


def generate_alerts(db: Session) -> dict[str, Any]:
    """Generate alerts from SLA, stale shipments and failed imports.

    The routine is idempotent: for each source there is at most one active alert.
    """
    processed_count = 0
    created_count = 0
    skipped_count = 0
    resolved_count = 0
    error_count = 0

    try:
        shipments = db.query(Shipment).filter(Shipment.is_active.is_(True)).all()
        for shipment in shipments:
            processed_count += 1
            try:
                created, skipped, resolved = _sync_shipment_alert(db, shipment)
                created_count += created
                skipped_count += skipped
                resolved_count += resolved
            except Exception as exc:  # pragma: no cover - defensive guard
                error_count += 1
                logger.exception("Failed to generate shipment alert for shipment=%s: %s", shipment.id, exc)

        failed_imports = (
            db.query(ImportHistory)
            .filter(func.lower(ImportHistory.status) == "failed")
            .all()
        )
        for history in failed_imports:
            processed_count += 1
            try:
                created, skipped, resolved = _sync_import_failure_alert(db, history)
                created_count += created
                skipped_count += skipped
                resolved_count += resolved
            except Exception as exc:  # pragma: no cover - defensive guard
                error_count += 1
                logger.exception("Failed to generate import alert for import=%s: %s", history.id, exc)

        db.commit()

        try:
            audit_log = AuditLogCreateRequest(
                event_type="alert_generated",
                entity_type="alert",
                action="create",
                source="system",
                severity="info",
                status="success",
                message=(
                    f"Alertas gerados: {created_count} criados, {resolved_count} resolvidos, {skipped_count} ignorados"
                ),
                metadata_json=(
                    f'{{"created_count": {created_count}, "resolved_count": {resolved_count}, '
                    f'"skipped_count": {skipped_count}, "processed_count": {processed_count}}}'
                ),
            )
            AuditLogService.create_log(db, audit_log)
        except Exception as exc:  # pragma: no cover - audit log should not break alerts
            logger.error("Failed to create audit log for alerts: %s", exc)

        return {
            "success": True,
            "processed_count": processed_count,
            "created_count": created_count,
            "skipped_count": skipped_count,
            "resolved_count": resolved_count,
            "error_count": error_count,
        }
    except Exception as exc:  # pragma: no cover - fatal path
        logger.exception("Failed to generate alerts: %s", exc)
        db.rollback()
        return {
            "success": False,
            "processed_count": processed_count,
            "created_count": created_count,
            "skipped_count": skipped_count,
            "resolved_count": resolved_count,
            "error_count": error_count + 1,
        }


def mark_alert_as_read(db: Session, alert_id: int) -> Alert:
    """Mark an alert as read and log the event."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Alert not found")

    if not alert.is_read:
        alert.is_read = True
        alert.read_at = datetime.now(UTC)
        _create_delivery_log(
            db,
            event_type="read",
            source_type=alert.source_type,
            source_id=alert.source_id,
            alert_type=alert.alert_type,
            alert=alert,
            delivery_status="success",
            message=f"Alerta {alert.id} marcado como lido",
        )
        db.commit()
    return alert


def mark_alert_as_resolved(db: Session, alert_id: int) -> Alert:
    """Mark an alert as resolved and log the event."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Alert not found")

    if not alert.is_resolved:
        alert.is_resolved = True
        alert.status = "resolved"
        alert.resolved_at = datetime.now(UTC)
        _create_delivery_log(
            db,
            event_type="resolved",
            source_type=alert.source_type,
            source_id=alert.source_id,
            alert_type=alert.alert_type,
            alert=alert,
            delivery_status="resolved",
            message=f"Alerta {alert.id} marcado como resolvido",
        )
        db.commit()
    return alert


def get_active_alerts_count(db: Session) -> int:
    """Get count of active alerts."""
    return db.query(Alert).filter(Alert.status == "active", Alert.is_resolved.is_(False)).count()


def get_no_update_alert_count(db: Session) -> int:
    """Count shipments that should raise the no-update alert."""
    count = 0
    shipments = db.query(Shipment).filter(Shipment.is_active.is_(True)).all()
    for shipment in shipments:
        try:
            sla_result = calculate_shipment_sla(db, shipment.id)
            sla_status = sla_result.get("sla_status")
            delay_days = sla_result.get("delay_days", 0)
            is_late = sla_result.get("is_late", False)
            exception_type = classify_exception_type(sla_status, shipment.criticality, is_late)
            alert_type, _, _, _ = _build_shipment_alert_details(
                shipment,
                sla_status,
                exception_type,
                delay_days,
            )
            if alert_type == "no_update":
                count += 1
        except Exception as exc:  # pragma: no cover - defensive guard
            logger.error("Failed to calculate no-update count for shipment=%s: %s", shipment.id, exc)
    return count
