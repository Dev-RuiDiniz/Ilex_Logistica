from pydantic import BaseModel


class ImportPreviewResponse(BaseModel):
    filename: str
    rows_received: int
    columns_detected: list[str]
    preview: list[dict[str, str]]
