from datetime import date, datetime

from pydantic import BaseModel


class ImportPreviewResponse(BaseModel):
    filename: str
    rows_received: int
    columns_detected: list[str]
    preview: list[dict[str, str]]


class ImportHistoryResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_hash: str
    rows_received: int
    duplicates_count: int
    imported_count: int
    rejected_count: int
    status: str
    created_at: datetime


class DeliveryListItem(BaseModel):
    id: int
    nf: str
    transportadora: str
    data_coleta: date
    valor_frete: float
    percentual_frete: float
    created_at: datetime


class DeliveryListResponse(BaseModel):
    items: list[DeliveryListItem]
    total: int
    page: int
    page_size: int


class DeliveryDetailResponse(BaseModel):
    id: int
    nf: str
    transportadora: str
    data_coleta: date
    valor_frete: float
    percentual_frete: float
    created_at: datetime
