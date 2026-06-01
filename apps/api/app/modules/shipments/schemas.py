from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class CSVRowError(BaseModel):
    row_number: int
    field: str | None = None
    message: str
    value: Any = None


class UploadResponse(BaseModel):
    import_id: int | None = None
    status: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: list[CSVRowError]


class ImportConfirmRequest(BaseModel):
    import_id: int = Field(gt=0)
    confirm: bool = Field(default=True)


class ImportConfirmResponse(BaseModel):
    import_id: int
    status: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    imported_count: int
    rejected_count: int
    errors: list[CSVRowError]


class ShipmentRowCreate(BaseModel):
    tracking_code: str = Field(min_length=1, max_length=100)
    carrier_name: str = Field(min_length=1, max_length=150)
    estimated_delivery: str
    recipient_name: str = Field(min_length=1, max_length=255)
    recipient_phone: str = Field(min_length=1, max_length=50)
    origin_address: str = Field(min_length=1)
    destination_address: str = Field(min_length=1)
    invoice_number: str | None = Field(default=None, max_length=50)
    invoice_key: str | None = Field(default=None, max_length=100)
    fiscal_document: str | None = Field(default=None, max_length=50)
    amount: str | None = Field(default=None)
    due_date: str | None = Field(default=None)

    @field_validator("estimated_delivery", "due_date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v or not v.strip():
            return None
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValueError("formato de data invalido, use ISO 8601 (YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: str | None) -> str | None:
        if not v or not v.strip():
            return None
        try:
            float(v.replace(",", ".").strip())
        except (ValueError, AttributeError):
            raise ValueError("valor monetario invalido")
        return v


class ShipmentListItem(BaseModel):
    id: int
    tracking_code: str
    carrier_id: int
    status: str
    estimated_delivery: datetime
    recipient_name: str
    recipient_phone: str
    origin_address: str
    destination_address: str
    invoice_number: str | None = None
    invoice_key: str | None = None
    fiscal_document: str | None = None
    amount: float | None = None
    due_date: datetime | None = None
    delay_days: int
    criticality: str
    created_at: datetime
    updated_at: datetime


class ShipmentListResponse(BaseModel):
    items: list[ShipmentListItem]
    total: int
    page: int
    page_size: int


class ShipmentDetailResponse(ShipmentListItem):
    pass


class ShipmentTreatmentCreate(BaseModel):
    status: str = Field(min_length=1, max_length=50)
    comment: str = Field(min_length=1)


class ShipmentTreatmentResponse(BaseModel):
    id: int
    shipment_id: int
    status: str
    comment: str
    created_by: int
    created_at: datetime
