from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.imports.models import ImportHistory
from app.modules.imports.schemas import (
    DeliveryDetailResponse,
    DeliveryListResponse,
    ImportConfirmRequest,
    ImportConfirmResponse,
    ImportHistoryResponse,
    ImportPreviewResponse,
    ImportPreviewV2Response,
    PromoteDeliveryRequest,
    PromoteDeliveryResponse,
)
from app.modules.imports.service import (
    get_delivery_detail,
    list_deliveries,
    parse_uploaded_file,
    persist_deliveries,
    persist_import_history,
    _validate_duplicate_nf_in_db,
    promote_delivery_to_shipment,
)
from app.modules.imports.service_v2 import confirm_import, preview_import

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/upload", response_model=ImportPreviewResponse)
def upload_import_file(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ImportPreviewResponse:
    """Legacy upload endpoint - persists immediately."""
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


@router.post("/preview", response_model=ImportPreviewV2Response)
def preview_import_endpoint(
    file: UploadFile = File(...),
    source: str | None = Query(default=None, description="Import source (e.g., braspress_assisted)"),
    db: Session = Depends(get_db),
) -> ImportPreviewV2Response:
    """BETA-012A: Preview import without persisting shipments.

    Creates a pending ImportHistory record with validated data in metadata.
    Validates all rows, detects duplicates, and returns detailed error/warning information.

    BETA-012C: Optional source parameter for layout-specific mapping (e.g., braspress_assisted).
    """
    preview = preview_import(db, file, source=source)
    response_dict = preview.to_dict()
    response_dict["import_id"] = preview.import_id
    response_dict["source"] = source  # BETA-012C: Include source in response
    return ImportPreviewV2Response(**response_dict)


@router.post("/confirm", response_model=ImportConfirmResponse)
def confirm_import_endpoint(
    request: ImportConfirmRequest,
    db: Session = Depends(get_db),
) -> ImportConfirmResponse:
    """BETA-012A: Confirm and persist import after preview.
    
    Only valid rows are persisted. Invalid rows cause the entire import to be rejected.
    """
    history = confirm_import(db, request.import_id)
    return ImportConfirmResponse(
        id=history.id,
        filename=history.filename,
        file_type=history.file_type,
        file_hash=history.file_hash,
        rows_received=history.rows_received,
        duplicates_count=history.duplicates_count,
        imported_count=history.imported_count,
        rejected_count=history.rejected_count,
        status=history.status,
        source=history.source,
        import_metadata=history.import_metadata,
        imported_by=history.imported_by,
        created_at=history.created_at,
        created_shipments=getattr(history, "created_shipment_ids", []),
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
            source=item.source,
            import_metadata=item.import_metadata,
            imported_by=item.imported_by,
        )
        for item in items
    ]


@router.get("/deliveries", response_model=DeliveryListResponse)
def list_deliveries_endpoint(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    nf: str | None = Query(default=None),
    transportadora: str | None = Query(default=None),
    data_coleta: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> DeliveryListResponse:
    return DeliveryListResponse(**list_deliveries(
        db=db,
        page=page,
        page_size=page_size,
        nf=nf,
        transportadora=transportadora,
        data_coleta=data_coleta,
    ))


@router.get("/deliveries/{delivery_id}", response_model=DeliveryDetailResponse)
def get_delivery_detail_endpoint(
    delivery_id: int,
    db: Session = Depends(get_db),
) -> DeliveryDetailResponse:
    detail = get_delivery_detail(db, delivery_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="entrega nao encontrada")
    return DeliveryDetailResponse(**detail)


# LOG-021: Endpoint para promover Delivery para Shipment
@router.post("/deliveries/{delivery_id}/promote", response_model=PromoteDeliveryResponse, status_code=201)
def promote_delivery_endpoint(
    delivery_id: int,
    request: PromoteDeliveryRequest,
    db: Session = Depends(get_db),
) -> PromoteDeliveryResponse:
    """Promove uma Delivery existente para Shipment."""
    shipment = promote_delivery_to_shipment(
        db=db,
        delivery_id=delivery_id,
        tracking_code=request.tracking_code,
        carrier_id=request.carrier_id,
        estimated_delivery=request.estimated_delivery,
        recipient_name=request.recipient_name,
        recipient_phone=request.recipient_phone,
        origin_address=request.origin_address,
        destination_address=request.destination_address,
        shipment_status=request.shipment_status,
    )
    return PromoteDeliveryResponse(**shipment)
