from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class QuoteInput(BaseModel):
    carrier_id: int
    status: str
    amount: Decimal | None = None
    transit_days: int | None = Field(default=None, ge=1)
    message: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_status_contract(self) -> "QuoteInput":
        if self.status not in {"quoted", "unavailable", "error"}:
            raise ValueError("status deve ser quoted, unavailable ou error")
        if self.status == "quoted" and (self.amount is None or self.amount <= 0):
            raise ValueError("quoted exige valor positivo")
        if self.status in {"unavailable", "error"} and self.amount is not None:
            raise ValueError("falha ou indisponibilidade nao aceita valor")
        return self


class QuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    carrier_id: int
    amount: Decimal | None
    transit_days: int | None
    status: str
    message: str | None
    source: str
    valid_until: datetime


class QuoteRoundResponse(BaseModel):
    id: int
    order_id: int
    sequence: int
    status: str
    expires_at: datetime
    recommended_quote_id: int | None
    selected_quote_id: int | None
    selection_mode: str | None
    selection_reason: str | None
    quotes: list[QuoteResponse]


class QuoteOverrideRequest(BaseModel):
    reason: str = Field(min_length=10, max_length=500)


class QuoteImportPreviewResponse(BaseModel):
    import_id: int
    file_hash: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: list[dict[str, object]]
    preview_items: list[dict[str, object]]


class QuoteImportConfirmRequest(BaseModel):
    import_id: int
