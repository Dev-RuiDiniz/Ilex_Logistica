"""Alerts router for BETA-017A."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.alerts.schemas import (
    AlertGenerationResponse,
    AlertListResponse,
    AlertMarkReadResponse,
    AlertMarkResolvedResponse,
    AlertResponse,
    AlertSummaryResponse,
    AlertDeliveryLogCreate,
    AlertDeliveryLogListResponse,
    AlertDeliveryLogResponse,
)
from app.modules.alerts.service import (
    generate_alerts,
    get_active_alerts_count,
    generate_no_update_alerts,
    generate_import_failure_alerts,
    create_delivery_log,
    update_delivery_log_status,
    get_pending_delivery_logs,
)
from app.modules.alerts.models import Alert, AlertDeliveryLog

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=AlertListResponse)
def list_alerts(
    status: str | None = Query(None, description="Filter by status"),
    severity: str | None = Query(None, description="Filter by severity"),
    alert_type: str | None = Query(None, description="Filter by alert type"),
    is_read: bool | None = Query(None, description="Filter by read status"),
    is_resolved: bool | None = Query(None, description="Filter by resolved status"),
    carrier_id: int | None = Query(None, description="Filter by carrier ID"),
    shipment_id: int | None = Query(None, description="Filter by shipment ID"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset results"),
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:read")),
) -> AlertListResponse:
    """List alerts with filters."""
    query = db.query(Alert)

    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    if is_read is not None:
        query = query.filter(Alert.is_read == is_read)
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    if carrier_id:
        query = query.filter(Alert.carrier_id == carrier_id)
    if shipment_id:
        query = query.filter(Alert.shipment_id == shipment_id)

    total = query.count()
    alerts = query.order_by(Alert.generated_at.desc()).offset(offset).limit(limit).all()

    return AlertListResponse(alerts=alerts, total=total)


@router.get("/summary", response_model=AlertSummaryResponse)
def get_alerts_summary(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:read")),
) -> AlertSummaryResponse:
    """Get alert summary with counters."""
    total_alerts = db.query(Alert).count()
    active_count = db.query(Alert).filter(
        Alert.status == "active",
        Alert.is_resolved.is_(False)
    ).count()
    read_count = db.query(Alert).filter(Alert.is_read.is_(True)).count()
    resolved_count = db.query(Alert).filter(Alert.is_resolved.is_(True)).count()
    critical_count = db.query(Alert).filter(Alert.severity == "critical").count()
    warning_count = db.query(Alert).filter(Alert.severity == "warning").count()
    info_count = db.query(Alert).filter(Alert.severity == "info").count()

    return AlertSummaryResponse(
        total_alerts=total_alerts,
        active_count=active_count,
        read_count=read_count,
        resolved_count=resolved_count,
        critical_count=critical_count,
        warning_count=warning_count,
        info_count=info_count,
    )


@router.post("/generate", response_model=AlertGenerationResponse)
def generate_alerts_endpoint(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertGenerationResponse:
    """Generate alerts from SLA and exceptions data."""
    result = generate_alerts(db)
    return AlertGenerationResponse(**result)


@router.patch("/{alert_id}/read", response_model=AlertMarkReadResponse)
def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertMarkReadResponse:
    """Mark an alert as read."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_read = True
    alert.read_at = datetime.now(UTC)
    alert.status = "read"
    db.commit()

    return AlertMarkReadResponse(success=True, message="Alert marked as read")


@router.patch("/{alert_id}/resolve", response_model=AlertMarkResolvedResponse)
def mark_alert_as_resolved(
    alert_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertMarkResolvedResponse:
    """Mark an alert as resolved."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_resolved = True
    alert.resolved_at = datetime.now(UTC)
    alert.status = "resolved"
    db.commit()

    return AlertMarkResolvedResponse(success=True, message="Alert marked as resolved")


@router.post("/generate/no-update", response_model=AlertGenerationResponse)
def generate_no_update_alerts_endpoint(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertGenerationResponse:
    """Generate alerts for shipments without updates."""
    result = generate_no_update_alerts(db)
    return AlertGenerationResponse(
        success=True,
        processed_count=result["created_count"] + result["skipped_count"],
        created_count=result["created_count"],
        skipped_count=result["skipped_count"],
        resolved_count=0,
        error_count=0,
    )


@router.post("/generate/import-failure", response_model=AlertGenerationResponse)
def generate_import_failure_alerts_endpoint(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertGenerationResponse:
    """Generate alerts for failed imports."""
    result = generate_import_failure_alerts(db)
    return AlertGenerationResponse(
        success=True,
        processed_count=result["created_count"] + result["skipped_count"],
        created_count=result["created_count"],
        skipped_count=result["skipped_count"],
        resolved_count=0,
        error_count=0,
    )


# Delivery Log endpoints
@router.post("/delivery-logs", response_model=AlertDeliveryLogResponse)
def create_delivery_log_endpoint(
    payload: AlertDeliveryLogCreate,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertDeliveryLogResponse:
    """Create a delivery log for alert notification."""
    log = create_delivery_log(
        db=db,
        alert_id=payload.alert_id,
        channel=payload.channel,
        recipient=payload.recipient,
        message=payload.message,
        subject=payload.subject,
        max_attempts=payload.max_attempts,
    )
    return AlertDeliveryLogResponse.model_validate(log)


@router.get("/delivery-logs", response_model=AlertDeliveryLogListResponse)
def list_delivery_logs(
    alert_id: int | None = Query(None, description="Filter by alert ID"),
    status: str | None = Query(None, description="Filter by status"),
    channel: str | None = Query(None, description="Filter by channel"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset results"),
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:read")),
) -> AlertDeliveryLogListResponse:
    """List delivery logs with filters."""
    query = db.query(AlertDeliveryLog)

    if alert_id:
        query = query.filter(AlertDeliveryLog.alert_id == alert_id)
    if status:
        query = query.filter(AlertDeliveryLog.status == status)
    if channel:
        query = query.filter(AlertDeliveryLog.channel == channel)

    total = query.count()
    logs = query.order_by(AlertDeliveryLog.created_at.desc()).offset(offset).limit(limit).all()

    return AlertDeliveryLogListResponse(logs=logs, total=total)


@router.get("/delivery-logs/pending", response_model=AlertDeliveryLogListResponse)
def get_pending_delivery_logs_endpoint(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:read")),
) -> AlertDeliveryLogListResponse:
    """Get pending delivery logs for processing."""
    logs = get_pending_delivery_logs(db)
    return AlertDeliveryLogListResponse(logs=logs, total=len(logs))


@router.patch("/delivery-logs/{log_id}", response_model=AlertDeliveryLogResponse)
def update_delivery_log_endpoint(
    log_id: int,
    status: str = Query(..., description="New status (pending, sent, failed)"),
    error_message: str | None = Query(None, description="Error message if failed"),
    sent: bool = Query(False, description="Whether the delivery was sent"),
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertDeliveryLogResponse:
    """Update delivery log status."""
    log = update_delivery_log_status(
        db=db,
        log_id=log_id,
        status=status,
        error_message=error_message,
        sent=sent,
    )
    if not log:
        raise HTTPException(status_code=404, detail="Delivery log not found")
    return AlertDeliveryLogResponse.model_validate(log)
