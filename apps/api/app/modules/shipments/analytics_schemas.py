from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CarrierEfficiencyMetrics(BaseModel):
    carrier_id: int
    carrier_name: str | None = None
    total_invoices: int
    total_shipments: int
    on_time_count: int
    on_time_percentage: float
    late_count: int
    late_percentage: float
    critical_count: int
    lost_count: int
    lost_percentage: float
    total_freight_value: float
    total_invoice_value: float
    average_freight_percentage: float
    financial_valid_count: int
    average_freight_value: float
    ranking_by_efficiency: int
    ranking_by_cost: int
    ranking_by_volume: int


class CarrierEfficiencyResponse(BaseModel):
    carriers: list[CarrierEfficiencyMetrics]
    generated_at: datetime


class ExceptionSummary(BaseModel):
    total_exceptions: int
    critical_count: int
    late_count: int
    warning_count: int
    unknown_sla_count: int


class ExceptionItem(BaseModel):
    shipment_id: int
    tracking_code: str
    invoice_number: str | None = None
    carrier_id: int
    carrier_name: str | None = None
    customer_name: str | None = None
    destination_uf: str | None = None
    status: str
    sla_status: str | None = None
    criticality: str
    delay_days: int
    sla_due_date: datetime | None = None
    exception_type: str
    exception_reason: str
    priority: int
    last_update_at: datetime


class ExceptionsPanelResponse(BaseModel):
    summary: ExceptionSummary
    items: list[ExceptionItem]
    filters_applied: dict[str, Any]
    generated_at: datetime
