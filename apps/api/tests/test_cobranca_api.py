"""Testes da API de cobrança (TDD RED)."""

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.integrations.mcp_whatsapp import McpWhatsAppClient
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from conftest import create_user_with_roles


def _login(client: TestClient, email: str, password: str) -> str:
    return client.post("/api/v1/auth/login", json={"email": email, "password": password}).json()["access_token"]


def _seed_overdue(db_session: Session, with_whatsapp: bool = True) -> Carrier:
    carrier = Carrier(name="Cob Carrier", whatsapp="+5511999999999" if with_whatsapp else None)
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    ship = Shipment(
        tracking_code=f"COB{int(datetime.now(UTC).timestamp())}",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=2),
        actual_delivery=None,
        recipient_name="Cliente",
        recipient_phone="+5511999999999",
        origin_address="O",
        destination_address="D",
        destination_uf="SP",
        customer_name="Cliente",
        delay_days=2,
    )
    db_session.add(ship)
    db_session.commit()
    return carrier


def test_cobranca_requires_auth(client: TestClient) -> None:
    response = client.post("/api/v1/shipments/cobranca/run", json={})
    assert response.status_code == 401


def test_cobranca_viewer_forbidden(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = _login(client, "viewer@ilex.com", "123456")
    response = client.post(
        "/api/v1/shipments/cobranca/run",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_cobranca_admin_runs(client: TestClient, db_session: Session, seed_roles: None) -> None:
    _seed_overdue(db_session, with_whatsapp=True)
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = _login(client, "admin@ilex.com", "123456")

    fake = McpWhatsAppClient.__new__(McpWhatsAppClient)
    fake.send_message = lambda *a, **k: {"status": "sent"}  # type: ignore

    import app.modules.shipments.router as router_module

    original = router_module.run_cobranca
    router_module.run_cobranca = lambda db, **kw: original(db, client=fake, **kw)  # type: ignore
    try:
        response = client.post(
            "/api/v1/shipments/cobranca/run",
            json={"dias_min": 1, "dias_max": 999},
            headers={"Authorization": f"Bearer {token}"},
        )
    finally:
        router_module.run_cobranca = original  # type: ignore

    assert response.status_code == 200
    body = response.json()
    assert body["enviadas"] == 1
    assert body["puladas_sem_whatsapp"] == 0


def test_cobranca_invalid_dias_max(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin2@ilex.com", "123456", ["admin"])
    token = _login(client, "admin2@ilex.com", "123456")
    response = client.post(
        "/api/v1/shipments/cobranca/run",
        json={"dias_min": 10, "dias_max": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
