from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


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
    average_freight_value: float
    ranking_by_efficiency: int
    ranking_by_cost: int
    ranking_by_volume: int


class CarrierEfficiencyResponse(BaseModel):
    carriers: list[CarrierEfficiencyMetrics]
    generated_at: datetime
