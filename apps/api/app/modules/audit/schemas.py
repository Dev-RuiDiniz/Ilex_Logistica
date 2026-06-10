"""Audit Log schemas for BETA-017A."""

from datetime import datetime

from pydantic import BaseModel, Field


class AuditLogBase(BaseModel):
    """Base schema for Audit Log."""

    event_type: str = Field(..., description="Type of event (e.g., 'shipment_created', 'alert_generated')")
    entity_type: str = Field(..., description="Type of entity (e.g., 'shipment', 'alert', 'import')")
    entity_id: int | None = Field(None, description="Entity ID")
    action: str = Field(..., description="Action performed (e.g., 'create', 'update', 'delete', 'read')")
    actor_user_id: int | None = Field(None, description="User ID who performed the action")
    actor_email: str | None = Field(None, description="Email of the user who performed the action")
    source: str | None = Field(None, description="Source of the action (e.g., 'api', 'system', 'import')")
    severity: str = Field(..., description="Severity level (e.g., 'info', 'warning', 'critical')")
    status: str = Field(..., description="Status of the action (e.g., 'success', 'failed', 'skipped')")
    message: str = Field(..., description="Log message")
    before_json: str | None = Field(None, description="JSON string with previous values")
    after_json: str | None = Field(None, description="JSON string with new values")
    metadata_json: str | None = Field(None, description="JSON string with additional metadata")
    request_id: str | None = Field(None, description="Request ID for correlation")
    ip_address: str | None = Field(None, description="IP address of the request")
    user_agent: str | None = Field(None, description="User agent of the request")


class AuditLogCreateRequest(AuditLogBase):
    """Schema for creating an audit log entry."""

    pass


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Schema for audit log list response."""

    logs: list[AuditLogResponse]
    total: int
    page: int
    page_size: int


class AuditLogSummaryResponse(BaseModel):
    """Schema for audit log summary response."""

    total_logs: int
    success_count: int
    failed_count: int
    skipped_count: int
    critical_count: int
    warning_count: int
    info_count: int
    create_count: int
    update_count: int
    delete_count: int
    read_count: int
