"""Audit Log router for BETA-017A."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.audit.schemas import (
    AuditLogCreateRequest,
    AuditLogListResponse,
    AuditLogResponse,
    AuditLogSummaryResponse,
)
from app.modules.audit.service import AuditLogService

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("", response_model=AuditLogResponse)
def create_audit_log(
    log_data: AuditLogCreateRequest,
    db: Session = Depends(get_db),
) -> AuditLogResponse:
    """Create a new audit log entry."""
    log = AuditLogService.create_log(db, log_data)
    return log


@router.get("", response_model=AuditLogListResponse)
def list_audit_logs(
    event_type: str | None = Query(None, description="Filter by event type"),
    entity_type: str | None = Query(None, description="Filter by entity type"),
    entity_id: int | None = Query(None, description="Filter by entity ID"),
    action: str | None = Query(None, description="Filter by action"),
    actor_user_id: int | None = Query(None, description="Filter by actor user ID"),
    severity: str | None = Query(None, description="Filter by severity"),
    status: str | None = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("audit:read")),
) -> AuditLogListResponse:
    """List audit logs with filters and pagination."""
    skip = (page - 1) * page_size
    logs, total = AuditLogService.get_logs(
        db,
        skip=skip,
        limit=page_size,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_user_id=actor_user_id,
        severity=severity,
        status=status,
    )

    return AuditLogListResponse(
        logs=logs,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/summary", response_model=AuditLogSummaryResponse)
def get_audit_summary(
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("audit:read")),
) -> AuditLogSummaryResponse:
    """Get audit log summary with statistics."""
    return AuditLogService.get_summary(db)


@router.get("/{log_id}", response_model=AuditLogResponse)
def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("audit:read")),
) -> AuditLogResponse:
    """Get a specific audit log by ID."""
    log = AuditLogService.get_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log
