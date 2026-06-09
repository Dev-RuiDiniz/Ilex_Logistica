"""Schemas do módulo dashboard para BETA-016A."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DashboardKpis(BaseModel):
    """KPIs do dashboard."""

    total_shipments: int
    on_time_count: int
    late_count: int
    critical_count: int
    warning_count: int
    unknown_sla_count: int
    resolved_count: int = 0  # Campo não existe no modelo, sempre 0
    no_update_count: int = 0  # Campo não existe no modelo, sempre 0
    exceptions_count: int
    import_failure_count: int
    active_alerts_count: int = 0  # Módulo de alertas não existe, sempre 0
    carriers_count: int


class DashboardCarrierEfficiencyItem(BaseModel):
    """Item de eficiência por transportadora."""

    carrier_id: int
    carrier_name: str | None
    total_shipments: int
    on_time_count: int
    late_count: int
    critical_count: int
    on_time_percentage: float
    ranking_by_efficiency: int


class DashboardExceptionItem(BaseModel):
    """Item de exceção."""

    shipment_id: int
    tracking_code: str
    invoice_number: str | None
    carrier_id: int
    carrier_name: str | None
    customer_name: str | None
    destination_uf: str | None
    status: str
    sla_status: str
    criticality: str
    delay_days: int
    sla_due_date: datetime | None
    exception_type: str | None
    exception_reason: str | None
    priority: int
    last_update_at: datetime


class DashboardFiltersApplied(BaseModel):
    """Filtros aplicados."""

    estimated_delivery_from: str | None = None
    estimated_delivery_to: str | None = None
    month: int | None = None
    year: int | None = None
    customer_name: str | None = None
    destination_uf: str | None = None
    carrier_id: int | None = None
    status: str | None = None
    criticality: str | None = None
    sla_status: str | None = None
    is_late: bool | None = None
    exception_type: str | None = None


class DashboardSummaryResponse(BaseModel):
    """Resposta do endpoint de dashboard summary."""

    kpis: DashboardKpis
    top_carriers_by_efficiency: list[DashboardCarrierEfficiencyItem]
    top_exceptions: list[DashboardExceptionItem]
    generated_at: datetime
    filters_applied: DashboardFiltersApplied
