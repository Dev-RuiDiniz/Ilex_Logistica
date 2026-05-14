from datetime import datetime

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
    status: str
    created_at: datetime
