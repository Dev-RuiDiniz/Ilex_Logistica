from fastapi import APIRouter, File, UploadFile

from app.modules.imports.schemas import ImportPreviewResponse
from app.modules.imports.service import parse_uploaded_file

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/upload", response_model=ImportPreviewResponse)
def upload_import_file(file: UploadFile = File(...)) -> ImportPreviewResponse:
    columns, rows = parse_uploaded_file(file)
    return ImportPreviewResponse(
        filename=file.filename or "unknown",
        rows_received=len(rows),
        columns_detected=columns,
        preview=rows[:5],
    )
