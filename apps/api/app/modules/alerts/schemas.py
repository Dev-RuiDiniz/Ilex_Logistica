"""Alerts schemas for BETA-017A."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertBase(BaseModel):
    """Base schema for Alert."""

    alert_type: str = Field(..., description="Type of alert")
    severity: str = Field(..., description="Severity level")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    source_type: str = Field(..., description="Source type")
    source_id: int | None = Field(None, description="Source ID")
    shipment_id: int | None = Field(None, description="Shipment ID")
    carrier_id: int | None = Field(None, description="Carrier ID")


class AlertCreate(AlertBase):
    """Schema for creating an alert."""

    pass


class AlertResponse(AlertBase):
    """Schema for alert response."""

    id: int
    status: str
    is_read: bool
    is_resolved: bool
    generated_at: datetime
    read_at: datetime | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertListResponse(BaseModel):
    """Schema for alert list response."""

    alerts: list[AlertResponse]
    total: int


class AlertSummaryResponse(BaseModel):
    """Schema for alert summary response."""

    total_alerts: int
    active_count: int
    read_count: int
    resolved_count: int
    critical_count: int
    warning_count: int
    info_count: int


class AlertGenerationResponse(BaseModel):
    """Schema for alert generation response."""

    success: bool
    processed_count: int
    created_count: int
    skipped_count: int
    resolved_count: int
    error_count: int


class AlertMarkReadResponse(BaseModel):
    """Schema for marking alert as read response."""

    success: bool
    message: str


class AlertMarkResolvedResponse(BaseModel):
    """Schema for marking alert as resolved response."""

    success: bool
    message: str


class AlertDeliveryLogBase(BaseModel):
    """Base schema for AlertDeliveryLog."""

    alert_id: int
    channel: str
    recipient: str
    subject: str | None = None
    message: str
    status: str = "pending"
    error_message: str | None = None
    attempts: int = 0
    max_attempts: int = 3


class AlertDeliveryLogCreate(AlertDeliveryLogBase):
    """Schema for creating an alert delivery log."""

    pass


class AlertDeliveryLogResponse(AlertDeliveryLogBase):
    """Schema for alert delivery log response."""

    id: int
    sent_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertDeliveryLogListResponse(BaseModel):
    """Schema for alert delivery log list response."""

    logs: list[AlertDeliveryLogResponse]
    total: int
