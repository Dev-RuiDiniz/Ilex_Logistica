"""Schemas for daily report API for BETA-018A."""

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class DailyReportGenerateRequest(BaseModel):
    """Request schema for generating a daily report."""

    report_date: datetime = Field(..., description="Date of the report")
    period_start: datetime | None = Field(None, description="Start of the period")
    period_end: datetime | None = Field(None, description="End of the period")
    generated_by_user_id: int | None = Field(None, description="ID of the user who generated the report")


class DailyReportSummary(BaseModel):
    """Summary of daily report."""

    total_shipments: int = Field(..., description="Total number of shipments")
    on_time_count: int = Field(..., description="Number of on-time shipments")
    late_count: int = Field(..., description="Number of late shipments")
    critical_count: int = Field(..., description="Number of critical shipments")
    warning_count: int = Field(..., description="Number of warning shipments")
    unknown_sla_count: int = Field(..., description="Number of shipments with unknown SLA")
    exceptions_count: int = Field(..., description="Number of exceptions")
    import_failure_count: int = Field(..., description="Number of import failures")
    carriers_count: int = Field(..., description="Number of carriers")


class DailyReportKpis(BaseModel):
    """KPIs of daily report."""

    active_alerts_count: int = Field(..., description="Number of active alerts")
    delivery_rate: float = Field(..., description="Delivery rate percentage")


class DailyReportExceptionItem(BaseModel):
    """Exception item in daily report."""

    shipment_id: int = Field(..., description="Shipment ID")
    tracking_code: str = Field(..., description="Tracking code")
    invoice_number: str | None = Field(None, description="Invoice number")
    carrier_id: int | None = Field(None, description="Carrier ID")
    carrier_name: str | None = Field(None, description="Carrier name")
    customer_name: str | None = Field(None, description="Customer name")
    destination_uf: str | None = Field(None, description="Destination UF")
    status: str | None = Field(None, description="Shipment status")
    sla_status: str | None = Field(None, description="SLA status")
    criticality: str | None = Field(None, description="Criticality")
    delay_days: int = Field(..., description="Delay in days")
    sla_due_date: datetime | None = Field(None, description="SLA due date")
    exception_type: str | None = Field(None, description="Exception type")
    exception_reason: str | None = Field(None, description="Exception reason")
    priority: int = Field(..., description="Priority")
    last_update_at: datetime | None = Field(None, description="Last update timestamp")


class DailyReportAlertItem(BaseModel):
    """Alert item in daily report."""

    id: int = Field(..., description="Alert ID")
    alert_type: str = Field(..., description="Alert type")
    severity: str = Field(..., description="Alert severity")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    source_type: str = Field(..., description="Source type")
    source_id: int | None = Field(None, description="Source ID")
    shipment_id: int | None = Field(None, description="Shipment ID")
    carrier_id: int | None = Field(None, description="Carrier ID")
    status: str = Field(..., description="Alert status")
    is_read: bool = Field(..., description="If alert is read")
    is_resolved: bool = Field(..., description="If alert is resolved")
    generated_at: datetime = Field(..., description="Generation timestamp")


class DailyReportCarrierEfficiencyItem(BaseModel):
    """Carrier efficiency item in daily report."""

    carrier_id: int = Field(..., description="Carrier ID")
    carrier_name: str = Field(..., description="Carrier name")
    total_shipments: int = Field(..., description="Total shipments")
    on_time_count: int = Field(..., description="On-time count")
    late_count: int = Field(..., description="Late count")
    efficiency: float = Field(..., description="Efficiency percentage")
    avg_cost: float | None = Field(None, description="Average cost")


class DailyReportImportFailures(BaseModel):
    """Import failures in daily report."""

    rejected_count: int = Field(..., description="Number of rejected records")


class DailyReportResponse(BaseModel):
    """Response schema for daily report."""

    id: int = Field(..., description="Report ID")
    report_date: datetime = Field(..., description="Report date")
    status: str = Field(..., description="Report status")
    generated_at: datetime = Field(..., description="Generation timestamp")
    generated_by_user_id: int | None = Field(None, description="ID of user who generated")
    period_start: datetime | None = Field(None, description="Period start")
    period_end: datetime | None = Field(None, description="Period end")
    summary_json: str = Field(..., description="Summary data as JSON string")
    kpis_json: str = Field(..., description="KPIs data as JSON string")
    exceptions_json: str = Field(..., description="Exceptions data as JSON string")
    alerts_json: str = Field(..., description="Alerts data as JSON string")
    carrier_efficiency_json: str = Field(..., description="Carrier efficiency data as JSON string")
    import_failures_json: str = Field(..., description="Import failures data as JSON string")
    notes: str | None = Field(None, description="Notes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")

    @classmethod
    def model_validate(cls, obj: Any) -> "DailyReportResponse":
        """Validate from database model."""
        return cls(
            id=obj.id,
            report_date=obj.report_date,
            status=obj.status,
            generated_at=obj.generated_at,
            generated_by_user_id=obj.generated_by_user_id,
            period_start=obj.period_start,
            period_end=obj.period_end,
            summary_json=obj.summary_json or "{}",
            kpis_json=obj.kpis_json or "{}",
            exceptions_json=obj.exceptions_json or "[]",
            alerts_json=obj.alerts_json or "[]",
            carrier_efficiency_json=obj.carrier_efficiency_json or "[]",
            import_failures_json=obj.import_failures_json or "{}",
            notes=obj.notes,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class DailyReportListResponse(BaseModel):
    """Response schema for listing daily reports."""

    reports: list[DailyReportResponse] = Field(..., description="List of reports")
    total: int = Field(..., description="Total count")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")
