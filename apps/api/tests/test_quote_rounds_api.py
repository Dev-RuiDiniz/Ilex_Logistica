from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.audit.models import OperationalAuditLog
from app.modules.carriers.models import Carrier
from app.modules.imports.models import ImportHistory
from app.modules.orders.models import FreightQuote, Order


def _seed_order(db: Session, user_id: int) -> Order:
    history = ImportHistory(
        filename="orders.csv", file_type="csv", file_hash="a" * 64, rows_received=1,
        imported_count=1, rejected_count=0, duplicates_count=0, status="CONFIRMED",
        source="orders_erp", imported_by=user_id,
    )
    db.add(history)
    db.flush()
    order = Order(
        source="erp", external_number="PED-1", order_date=date(2026, 7, 3), customer_name="Cliente",
        origin_zip="01310100", origin_uf="SP", destination_zip="20040002", destination_uf="RJ",
        weight_kg=Decimal("10.5"), volume_count=2, goods_value=Decimal("1200"), currency="BRL",
        status="active", import_history_id=history.id, created_by=user_id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def test_round_collects_active_carriers_and_preserves_individual_failures(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    user_id = db_session.query(ImportHistory).count() + 1
    order = _seed_order(db_session, user_id)
    active = Carrier(name="Ativa", external_code="ATIVA", is_active=True)
    other = Carrier(name="Outra", external_code="OUTRA", is_active=True)
    inactive = Carrier(name="Inativa", external_code="INATIVA", is_active=False)
    db_session.add_all([active, other, inactive])
    db_session.commit()

    created = client.post(f"/api/v1/orders/{order.id}/quote-rounds", headers=auth_headers)
    assert created.status_code == 201
    round_id = created.json()["id"]
    assert len(created.json()["quotes"]) == 2

    failed = client.post(
        f"/api/v1/quote-rounds/{round_id}/quotes",
        headers=auth_headers,
        json={"carrier_id": active.id, "status": "error", "message": "portal indisponivel"},
    )
    quoted = client.post(
        f"/api/v1/quote-rounds/{round_id}/quotes",
        headers=auth_headers,
        json={"carrier_id": other.id, "status": "quoted", "amount": "99.90", "transit_days": 2},
    )
    assert failed.status_code == quoted.status_code == 200
    assert quoted.json()["recommended_quote_id"] == quoted.json()["selected_quote_id"]
    assert quoted.json()["status"] == "completed"
    assert db_session.query(FreightQuote).filter(FreightQuote.status == "error").count() == 1


def test_override_requires_reason_and_is_audited(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    order = _seed_order(db_session, 1)
    carriers = [Carrier(name=f"Carrier {index}", is_active=True) for index in (1, 2)]
    db_session.add_all(carriers)
    db_session.commit()
    round_id = client.post(f"/api/v1/orders/{order.id}/quote-rounds", headers=auth_headers).json()["id"]
    for carrier, amount in zip(carriers, ("90", "100"), strict=True):
        response = client.post(
            f"/api/v1/quote-rounds/{round_id}/quotes", headers=auth_headers,
            json={"carrier_id": carrier.id, "status": "quoted", "amount": amount, "transit_days": 2},
        )
        assert response.status_code == 200
    expensive = db_session.query(FreightQuote).filter(FreightQuote.carrier_id == carriers[1].id).one()

    rejected = client.post(
        f"/api/v1/quote-rounds/{round_id}/select/{expensive.id}", headers=auth_headers,
        json={"reason": "curta"},
    )
    accepted = client.post(
        f"/api/v1/quote-rounds/{round_id}/select/{expensive.id}", headers=auth_headers,
        json={"reason": "Preferencia operacional documentada"},
    )
    assert rejected.status_code == 422
    assert accepted.status_code == 200
    body = accepted.json()
    assert body["selected_quote_id"] == expensive.id
    assert body["recommended_quote_id"] != expensive.id
    assert db_session.query(OperationalAuditLog).filter_by(event_type="quote_override").count() == 1


def test_quote_csv_preview_and_confirm_are_transactional(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    order = _seed_order(db_session, 1)
    carriers = [
        Carrier(name="CSV 1", external_code="CSV1", is_active=True),
        Carrier(name="CSV 2", external_code="CSV2", is_active=True),
    ]
    db_session.add_all(carriers)
    db_session.commit()
    round_id = client.post(f"/api/v1/orders/{order.id}/quote-rounds", headers=auth_headers).json()["id"]
    content = (
        "round_id,carrier_external_code,status,amount,transit_days,message\n"
        f"{round_id},CSV1,quoted,88.50,2,ok\n"
        f"{round_id},CSV2,error,,,sem cobertura\n"
    )
    preview = client.post(
        f"/api/v1/quote-rounds/{round_id}/quotes/import/preview",
        headers=auth_headers,
        files={"file": ("quotes.csv", content.encode(), "text/csv")},
    )
    assert preview.status_code == 200
    assert preview.json()["valid_rows"] == 2
    assert db_session.query(FreightQuote).filter(FreightQuote.status == "pending").count() == 2
    confirmed = client.post(
        f"/api/v1/quote-rounds/{round_id}/quotes/import/confirm",
        headers=auth_headers,
        json={"import_id": preview.json()["import_id"]},
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["status"] == "completed"
    assert {quote["source"] for quote in confirmed.json()["quotes"]} == {"csv"}
