from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict


class OrderRowError(BaseModel):
    row_number: int
    field: str | None = None
    message: str
    value: Any = None


class OrderImportPreviewResponse(BaseModel):
    import_id: int
    filename: str
    file_hash: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    preview_items: list[dict[str, Any]]
    errors: list[OrderRowError]
    warnings: list[OrderRowError]


class OrderImportConfirmRequest(BaseModel):
    import_id: int


class OrderImportResultResponse(BaseModel):
    id: int
    filename: str
    file_hash: str
    rows_received: int
    imported_count: int
    rejected_count: int
    duplicates_count: int
    status: str
    created_at: datetime


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    external_number: str
    order_date: date
    customer_name: str
    origin_zip: str
    origin_uf: str
    destination_zip: str
    destination_uf: str
    weight_kg: Decimal
    volume_count: int
    goods_value: Decimal
    currency: str
    status: str
    import_history_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int
