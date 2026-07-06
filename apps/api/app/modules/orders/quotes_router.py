from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.orders.quote_schemas import (
    QuoteImportConfirmRequest,
    QuoteImportPreviewResponse,
    QuoteInput,
    QuoteOverrideRequest,
    QuoteRoundResponse,
)
from app.modules.orders.quote_service import (
    confirm_quote_import,
    get_quote_round,
    override_quote,
    register_quote,
    round_payload,
    preview_quote_import,
)
from app.modules.users.models import User

router = APIRouter(prefix="/quote-rounds", tags=["quote-rounds"])


@router.get("/{round_id}", response_model=QuoteRoundResponse)
def read_round(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:read")),
) -> QuoteRoundResponse:
    return QuoteRoundResponse(**round_payload(db, get_quote_round(db, round_id)))


@router.post("/{round_id}/quotes", response_model=QuoteRoundResponse)
def write_quote(
    round_id: int,
    request: QuoteInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:write")),
) -> QuoteRoundResponse:
    quote_round = register_quote(
        db,
        round_id,
        request.carrier_id,
        request.status,
        request.amount,
        request.transit_days,
        request.message,
        current_user.id,
        current_user.email,
    )
    return QuoteRoundResponse(**round_payload(db, quote_round))


@router.post("/{round_id}/select/{quote_id}", response_model=QuoteRoundResponse)
def select_quote(
    round_id: int,
    quote_id: int,
    request: QuoteOverrideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:override")),
) -> QuoteRoundResponse:
    quote_round = override_quote(db, round_id, quote_id, request.reason, current_user.id, current_user.email)
    return QuoteRoundResponse(**round_payload(db, quote_round))


@router.post("/{round_id}/quotes/import/preview", response_model=QuoteImportPreviewResponse)
def preview_quotes_csv(
    round_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:write")),
) -> QuoteImportPreviewResponse:
    raw = file.file.read(20 * 1024 * 1024 + 1)
    if len(raw) > 20 * 1024 * 1024:
        from fastapi import HTTPException

        raise HTTPException(status_code=413, detail="arquivo excede 20 MB")
    return QuoteImportPreviewResponse(
        **preview_quote_import(db, round_id, file.filename or "quotes.csv", raw, current_user.id)
    )


@router.post("/{round_id}/quotes/import/confirm", response_model=QuoteRoundResponse)
def confirm_quotes_csv(
    round_id: int,
    request: QuoteImportConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("quotes:write")),
) -> QuoteRoundResponse:
    quote_round = confirm_quote_import(db, round_id, request.import_id, current_user.id, current_user.email)
    return QuoteRoundResponse(**round_payload(db, quote_round))
