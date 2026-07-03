from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.imports.models import ImportHistory
from app.modules.orders.models import Order
from app.modules.orders.schemas import (
    OrderImportConfirmRequest,
    OrderImportPreviewResponse,
    OrderImportResultResponse,
    OrderListResponse,
    OrderResponse,
)
from app.modules.orders.service import confirm_order_import, list_orders, preview_order_import
from app.modules.orders.quote_schemas import QuoteRoundResponse
from app.modules.orders.quote_service import create_quote_round, list_quote_rounds, round_payload
from app.modules.users.models import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/imports/preview", response_model=OrderImportPreviewResponse)
def preview_orders(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders:write")),
) -> OrderImportPreviewResponse:
    return OrderImportPreviewResponse(**preview_order_import(db, file, current_user.id))


@router.post("/imports/confirm", response_model=OrderImportResultResponse)
def confirm_orders(
    request: OrderImportConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders:write")),
) -> OrderImportResultResponse:
    return OrderImportResultResponse.model_validate(
        confirm_order_import(db, request.import_id, current_user.id), from_attributes=True
    )


@router.get("/imports/{import_id}", response_model=OrderImportResultResponse)
def get_order_import(
    import_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders:read")),
) -> OrderImportResultResponse:
    history = db.get(ImportHistory, import_id)
    if history is None or history.source != "orders_erp":
        raise HTTPException(status_code=404, detail="importacao nao encontrada")
    return OrderImportResultResponse.model_validate(history, from_attributes=True)


@router.get("", response_model=OrderListResponse)
def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    source: str | None = Query(None),
    external_number: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders:read")),
) -> OrderListResponse:
    return OrderListResponse(**list_orders(db, page, page_size, status, source, external_number))


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders:read")),
) -> OrderResponse:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="pedido nao encontrado")
    return OrderResponse.model_validate(order)


@router.post("/{order_id}/quote-rounds", response_model=QuoteRoundResponse, status_code=201)
def start_quote_round(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:write")),
) -> QuoteRoundResponse:
    quote_round = create_quote_round(db, order_id, current_user.id, current_user.email)
    return QuoteRoundResponse(**round_payload(db, quote_round))


@router.get("/{order_id}/quote-rounds", response_model=list[QuoteRoundResponse])
def get_order_quote_rounds(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:read")),
) -> list[QuoteRoundResponse]:
    return [QuoteRoundResponse(**round_payload(db, item)) for item in list_quote_rounds(db, order_id)]
