"""Alerts router for BETA-017A."""

from fastapi import APIRouter, Depends, Query
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
)
from app.modules.alerts.service import generate_alerts, get_active_alerts_count, mark_alert_as_read as mark_alert_as_read_service, mark_alert_as_resolved as mark_alert_as_resolved_service
from app.modules.alerts.models import Alert

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
    mark_alert_as_read_service(db, alert_id)
    return AlertMarkReadResponse(success=True, message="Alert marked as read")


@router.patch("/{alert_id}/resolve", response_model=AlertMarkResolvedResponse)
def mark_alert_as_resolved(
    alert_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("alerts:write")),
) -> AlertMarkResolvedResponse:
    """Mark an alert as resolved."""
    mark_alert_as_resolved_service(db, alert_id)
    return AlertMarkResolvedResponse(success=True, message="Alert marked as resolved")
