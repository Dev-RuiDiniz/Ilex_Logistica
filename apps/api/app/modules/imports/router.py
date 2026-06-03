from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.imports.models import ImportHistory
from app.modules.imports.schemas import ImportHistoryResponse, ImportPreviewResponse
from app.modules.imports.service import parse_uploaded_file, persist_deliveries, persist_import_history, _validate_duplicate_nf_in_db

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/upload", response_model=ImportPreviewResponse)
def upload_import_file(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ImportPreviewResponse:
    columns, rows, file_type, file_hash = parse_uploaded_file(file)
    # LOG-010: validar duplicidade no banco
    duplicates_count = _validate_duplicate_nf_in_db(db, rows)
    persist_deliveries(db, rows)
    persist_import_history(
        db,
        filename=file.filename or "unknown",
        file_type=file_type,
        file_hash=file_hash,
        rows_received=len(rows),
        imported_count=len(rows),
        rejected_count=0,
        duplicates_count=duplicates_count,
        status="SUCCESS",
    )
    return ImportPreviewResponse(
        filename=file.filename or "unknown",
        rows_received=len(rows),
        columns_detected=columns,
        preview=rows[:5],
    )


@router.get("/history", response_model=list[ImportHistoryResponse])
def list_import_history(
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[ImportHistoryResponse]:
    items = (
        db.query(ImportHistory).order_by(ImportHistory.created_at.desc(), ImportHistory.id.desc()).limit(limit).all()
    )
    return [
        ImportHistoryResponse(
            id=item.id,
            filename=item.filename,
            file_type=item.file_type,
            file_hash=item.file_hash,
            rows_received=item.rows_received,
            duplicates_count=item.duplicates_count,
            imported_count=item.imported_count,
            rejected_count=item.rejected_count,
            status=item.status,
            created_at=item.created_at,
        )
        for item in items
    ]
