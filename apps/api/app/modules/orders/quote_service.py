import csv
import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from io import StringIO
from typing import Any

from pydantic import ValidationError

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.audit.models import OperationalAuditLog
from app.modules.carriers.models import Carrier
from app.modules.imports.models import ImportHistory
from app.modules.orders.models import FreightQuote, Order, QuoteRound
from app.modules.orders.quote_schemas import QuoteInput
from app.modules.shipments.models import Shipment


def choose_best_quote(
    quotes: list[FreightQuote], efficiencies: dict[int, Decimal], now: datetime
) -> FreightQuote | None:
    valid = [
        quote
        for quote in quotes
        if quote.status == "quoted"
        and quote.amount is not None
        and _as_utc(quote.valid_until) > _as_utc(now)
    ]
    if not valid:
        return None
    return min(
        valid,
        key=lambda quote: (
            Decimal(quote.amount),
            quote.transit_days if quote.transit_days is not None else 2**31 - 1,
            -efficiencies.get(quote.carrier_id, Decimal("0")),
            quote.carrier_id,
        ),
    )


def create_quote_round(db: Session, order_id: int, user_id: int, actor_email: str | None) -> QuoteRound:
    order = db.get(Order, order_id)
    if order is None or order.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pedido ativo nao encontrado")
    sequence = (db.query(func.max(QuoteRound.sequence)).filter(QuoteRound.order_id == order_id).scalar() or 0) + 1
    expires_at = datetime.now(UTC) + timedelta(hours=24)
    quote_round = QuoteRound(
        order_id=order_id, sequence=sequence, status="open", expires_at=expires_at, created_by=user_id
    )
    db.add(quote_round)
    db.flush()
    carriers = db.query(Carrier).filter(Carrier.is_active.is_(True)).order_by(Carrier.id).all()
    for carrier in carriers:
        db.add(
            FreightQuote(
                round_id=quote_round.id,
                carrier_id=carrier.id,
                status="pending",
                source="web",
                valid_until=expires_at,
                created_by=user_id,
            )
        )
    _add_audit(db, "quote_round_created", "quote_round", quote_round.id, "create", user_id, actor_email)
    db.commit()
    db.refresh(quote_round)
    return quote_round


def register_quote(
    db: Session,
    round_id: int,
    carrier_id: int,
    quote_status: str,
    amount: Decimal | None,
    transit_days: int | None,
    message: str | None,
    user_id: int,
    actor_email: str | None,
    source: str = "web",
) -> QuoteRound:
    quote_round = _get_round(db, round_id)
    if _as_utc(quote_round.expires_at) <= datetime.now(UTC):
        quote_round.status = "expired"
        db.commit()
        raise HTTPException(status_code=409, detail="rodada vencida")
    quote = (
        db.query(FreightQuote)
        .filter(FreightQuote.round_id == round_id, FreightQuote.carrier_id == carrier_id)
        .one_or_none()
    )
    if quote is None:
        raise HTTPException(status_code=404, detail="transportadora nao participa da rodada")
    quote.status = quote_status
    quote.amount = amount
    quote.transit_days = transit_days
    quote.message = _sanitize_message(message)
    quote.source = source
    quote.valid_until = quote_round.expires_at
    previous_round_status = quote_round.status
    _recalculate_round(db, quote_round)
    _add_audit(db, "freight_quote_recorded", "freight_quote", quote.id, "update", user_id, actor_email)
    if previous_round_status == "open" and quote_round.status != "open":
        _add_audit(db, "quote_round_completed", "quote_round", round_id, "update", user_id, actor_email)
    db.commit()
    db.refresh(quote_round)
    return quote_round


def override_quote(
    db: Session, round_id: int, quote_id: int, reason: str, user_id: int, actor_email: str | None
) -> QuoteRound:
    quote_round = _get_round(db, round_id)
    quote = db.get(FreightQuote, quote_id)
    if (
        quote is None
        or quote.round_id != round_id
        or quote.status != "quoted"
        or quote.amount is None
        or _as_utc(quote.valid_until) <= datetime.now(UTC)
    ):
        raise HTTPException(status_code=409, detail="cotacao invalida ou vencida")
    before = quote_round.selected_quote_id
    quote_round.selected_quote_id = quote.id
    quote_round.selection_mode = "manual"
    quote_round.selection_reason = _sanitize_message(reason)
    quote_round.selected_by = user_id
    _add_audit(
        db,
        "quote_override",
        "quote_round",
        quote_round.id,
        "update",
        user_id,
        actor_email,
        before={"selected_quote_id": before},
        after={"selected_quote_id": quote.id, "reason": quote_round.selection_reason},
    )
    db.commit()
    db.refresh(quote_round)
    return quote_round


def preview_quote_import(db: Session, round_id: int, filename: str, raw: bytes, user_id: int) -> dict[str, Any]:
    _get_round(db, round_id)
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="use arquivo CSV")
    try:
        reader = csv.DictReader(StringIO(raw.decode("utf-8-sig")))
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV deve usar UTF-8") from exc
    required = {"round_id", "carrier_external_code", "status", "amount", "transit_days", "message"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(status_code=400, detail="cabecalho de cotacoes invalido")
    carriers = {
        carrier.external_code: carrier
        for carrier in db.query(Carrier).filter(Carrier.external_code.is_not(None)).all()
    }
    participants = {
        quote.carrier_id
        for quote in db.query(FreightQuote).filter(FreightQuote.round_id == round_id).all()
    }
    valid_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    preview: list[dict[str, Any]] = []
    for row_number, row in enumerate(reader, start=2):
        row_errors: list[dict[str, Any]] = []
        carrier = carriers.get((row.get("carrier_external_code") or "").strip())
        try:
            csv_round_id = int(row.get("round_id") or "")
        except ValueError:
            csv_round_id = 0
        if csv_round_id != round_id:
            row_errors.append({"row_number": row_number, "field": "round_id", "message": "rodada divergente"})
        if carrier is None or carrier.id not in participants:
            row_errors.append(
                {"row_number": row_number, "field": "carrier_external_code", "message": "transportadora invalida"}
            )
        try:
            quote_input = QuoteInput(
                carrier_id=carrier.id if carrier else 0,
                status=(row.get("status") or "").strip(),
                amount=(row.get("amount") or "").strip() or None,
                transit_days=(row.get("transit_days") or "").strip() or None,
                message=(row.get("message") or "").strip() or None,
            )
        except ValidationError as exc:
            row_errors.append({"row_number": row_number, "field": None, "message": exc.errors()[0]["msg"]})
            quote_input = None
        if row_errors:
            errors.extend(row_errors)
        elif quote_input is not None:
            valid_rows.append(quote_input.model_dump(mode="json"))
        preview.append({"row_number": row_number, "data": row, "errors": row_errors, "is_valid": not row_errors})
    if not preview:
        raise HTTPException(status_code=400, detail="CSV sem linhas")
    file_hash = hashlib.sha256(raw).hexdigest()
    history = ImportHistory(
        filename=filename,
        file_type="csv",
        file_hash=file_hash,
        rows_received=len(preview),
        duplicates_count=0,
        imported_count=0,
        rejected_count=len(errors),
        status="PENDING",
        source=f"quote_round:{round_id}",
        import_metadata=json.dumps({"rows": valid_rows, "errors": errors}, ensure_ascii=False),
        imported_by=user_id,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return {
        "import_id": history.id,
        "file_hash": file_hash,
        "total_rows": len(preview),
        "valid_rows": len(valid_rows),
        "invalid_rows": len(preview) - len(valid_rows),
        "errors": errors,
        "preview_items": preview[:10],
    }


def confirm_quote_import(
    db: Session, round_id: int, import_id: int, user_id: int, actor_email: str | None
) -> QuoteRound:
    quote_round = _get_round(db, round_id)
    history = db.get(ImportHistory, import_id)
    if history is None or history.source != f"quote_round:{round_id}":
        raise HTTPException(status_code=404, detail="preview de cotacoes nao encontrado")
    if history.status == "CONFIRMED":
        return quote_round
    payload = json.loads(history.import_metadata or "{}")
    try:
        for row in payload.get("rows", []):
            quote = (
                db.query(FreightQuote)
                .filter(FreightQuote.round_id == round_id, FreightQuote.carrier_id == row["carrier_id"])
                .one()
            )
            quote.status = row["status"]
            quote.amount = Decimal(row["amount"]) if row.get("amount") is not None else None
            quote.transit_days = row.get("transit_days")
            quote.message = _sanitize_message(row.get("message"))
            quote.source = "csv"
            _add_audit(db, "freight_quote_imported", "freight_quote", quote.id, "update", user_id, actor_email)
        previous_round_status = quote_round.status
        _recalculate_round(db, quote_round)
        history.imported_count = len(payload.get("rows", []))
        history.status = "CONFIRMED"
        _add_audit(db, "quote_import_confirmed", "quote_round", round_id, "update", user_id, actor_email)
        if previous_round_status == "open" and quote_round.status != "open":
            _add_audit(db, "quote_round_completed", "quote_round", round_id, "update", user_id, actor_email)
        db.commit()
        db.refresh(quote_round)
        return quote_round
    except Exception:
        db.rollback()
        raise


def get_quote_round(db: Session, round_id: int) -> QuoteRound:
    quote_round = _get_round(db, round_id)
    if quote_round.status == "open" and _as_utc(quote_round.expires_at) <= datetime.now(UTC):
        quote_round.status = "expired"
        db.query(FreightQuote).filter(
            FreightQuote.round_id == round_id, FreightQuote.status.in_(["pending", "quoted"])
        ).update({FreightQuote.status: "expired"}, synchronize_session=False)
        db.commit()
        db.refresh(quote_round)
    return quote_round


def list_quote_rounds(db: Session, order_id: int) -> list[QuoteRound]:
    if db.get(Order, order_id) is None:
        raise HTTPException(status_code=404, detail="pedido nao encontrado")
    return db.query(QuoteRound).filter(QuoteRound.order_id == order_id).order_by(QuoteRound.sequence.desc()).all()


def round_payload(db: Session, quote_round: QuoteRound) -> dict[str, Any]:
    quotes = db.query(FreightQuote).filter(FreightQuote.round_id == quote_round.id).order_by(FreightQuote.carrier_id).all()
    return {
        "id": quote_round.id,
        "order_id": quote_round.order_id,
        "sequence": quote_round.sequence,
        "status": quote_round.status,
        "expires_at": quote_round.expires_at,
        "recommended_quote_id": quote_round.recommended_quote_id,
        "selected_quote_id": quote_round.selected_quote_id,
        "selection_mode": quote_round.selection_mode,
        "selection_reason": quote_round.selection_reason,
        "quotes": quotes,
    }


def _recalculate_round(db: Session, quote_round: QuoteRound) -> None:
    db.flush()
    quotes = db.query(FreightQuote).filter(FreightQuote.round_id == quote_round.id).all()
    efficiencies = _carrier_efficiencies(db, {quote.carrier_id for quote in quotes})
    best = choose_best_quote(quotes, efficiencies, datetime.now(UTC))
    quote_round.recommended_quote_id = best.id if best else None
    if quote_round.selection_mode != "manual":
        quote_round.selected_quote_id = best.id if best else None
        quote_round.selection_mode = "automatic" if best else None
    if all(quote.status != "pending" for quote in quotes):
        quote_round.status = "completed" if best else "no_valid_quotes"
    else:
        quote_round.status = "open"


def _carrier_efficiencies(db: Session, carrier_ids: set[int]) -> dict[int, Decimal]:
    metrics = {carrier_id: [0, 0] for carrier_id in carrier_ids}
    shipments = (
        db.query(Shipment)
        .filter(Shipment.carrier_id.in_(carrier_ids), Shipment.actual_delivery.is_not(None))
        .all()
        if carrier_ids
        else []
    )
    for shipment in shipments:
        metrics[shipment.carrier_id][1] += 1
        if shipment.actual_delivery <= shipment.estimated_delivery:
            metrics[shipment.carrier_id][0] += 1
    return {
        carrier_id: Decimal(on_time * 100) / Decimal(total) if total else Decimal("0")
        for carrier_id, (on_time, total) in metrics.items()
    }


def _get_round(db: Session, round_id: int) -> QuoteRound:
    quote_round = db.get(QuoteRound, round_id)
    if quote_round is None:
        raise HTTPException(status_code=404, detail="rodada nao encontrada")
    return quote_round


def _sanitize_message(message: str | None) -> str | None:
    if message is None:
        return None
    return re.sub(r"<[^>]*>", "", message).strip()[:500]


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _add_audit(
    db: Session,
    event_type: str,
    entity_type: str,
    entity_id: int,
    action: str,
    user_id: int,
    actor_email: str | None,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
) -> None:
    db.add(
        OperationalAuditLog(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            actor_user_id=user_id,
            actor_email=actor_email,
            source="api",
            severity="info",
            status="success",
            message=event_type,
            before_json=json.dumps(before) if before else None,
            after_json=json.dumps(after) if after else None,
        )
    )
