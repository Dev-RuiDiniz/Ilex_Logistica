from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.shipments.schemas import ImportConfirmRequest, ImportConfirmResponse, ShipmentListResponse, UploadResponse
from app.modules.shipments.service import list_shipments, parse_csv_file, process_import

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("", response_model=ShipmentListResponse)
def list_shipments_endpoint(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[str | None, Query()] = None,
    carrier_id: Annotated[int | None, Query()] = None,
    tracking_code: Annotated[str | None, Query()] = None,
    invoice_number: Annotated[str | None, Query()] = None,
    fiscal_document: Annotated[str | None, Query()] = None,
    criticality: Annotated[str | None, Query()] = None,
    estimated_delivery_from: Annotated[str | None, Query()] = None,
    estimated_delivery_to: Annotated[str | None, Query()] = None,
    due_date_from: Annotated[str | None, Query()] = None,
    due_date_to: Annotated[str | None, Query()] = None,
    sort_by: Annotated[str, Query()] = "created_at",
    sort_order: Annotated[str, Query()] = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ShipmentListResponse:
    return list_shipments(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        carrier_id=carrier_id,
        tracking_code=tracking_code,
        invoice_number=invoice_number,
        fiscal_document=fiscal_document,
        criticality=criticality,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_csv(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UploadResponse:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="arquivo deve ser CSV")

    try:
        file_content = file.file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="erro ao ler arquivo")

    result = parse_csv_file(file_content, db, current_user.id, file.filename)

    return UploadResponse(**result)


@router.post("/import")
def confirm_import(
    payload: ImportConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ImportConfirmResponse:
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="confirm deve ser true")

    result = process_import(payload.import_id, db)

    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result["errors"][0].message if result["errors"] else "erro ao processar importacao")

    return ImportConfirmResponse(**result)
