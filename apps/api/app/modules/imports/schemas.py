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


# LOG-021: Schema para promoção Delivery → Shipment
class PromoteDeliveryRequest(BaseModel):
    tracking_code: str
    carrier_id: int
    estimated_delivery: datetime
    recipient_name: str
    recipient_phone: str
    origin_address: str
    destination_address: str
    shipment_status: str = "pending"


class PromoteDeliveryResponse(BaseModel):
    id: int
    tracking_code: str
    carrier_id: int
    status: str
    estimated_delivery: datetime
    recipient_name: str
    recipient_phone: str
    origin_address: str
    destination_address: str
    amount: float | None
    invoice_number: str | None
    created_at: datetime
    updated_at: datetime
