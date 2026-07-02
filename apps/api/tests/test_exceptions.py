from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def seed_shipments(db_session: Session) -> None:
    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    now = datetime.now(UTC)
    rows = [
        Shipment(
            tracking_code="TRK-NORMAL",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=now,
            recipient_name="A",
            recipient_phone="1",
            origin_address="orig",
            destination_address="dest",
            delay_days=0,
            criticality="normal",
            meta_data="{}",
            is_active=True,
        ),
        Shipment(
            tracking_code="TRK-ATRASO",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=now - timedelta(days=2),
            recipient_name="B",
            recipient_phone="2",
            origin_address="orig",
            destination_address="dest",
            delay_days=2,
            criticality="baixa",
            meta_data="{}",
            is_active=True,
        ),
        Shipment(
            tracking_code="TRK-ALTA",
            carrier_id=carrier.id,
            status="in_transit",
            estimated_delivery=now - timedelta(days=40),
            recipient_name="C",
            recipient_phone="3",
            origin_address="orig",
            destination_address="dest",
            delay_days=40,
            criticality="alta",
            meta_data="{}",
            is_active=True,
        ),
    ]
    db_session.add_all(rows)
    db_session.commit()


def test_exceptions_lista_apenas_itens_em_excecao(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")
    seed_shipments(db_session)

    response = client.get("/api/v1/shipments/exceptions", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 2
    tracking_codes = {item["tracking_code"] for item in body["items"]}
    assert "TRK-NORMAL" not in tracking_codes
    assert {"TRK-ATRASO", "TRK-ALTA"} == tracking_codes


def test_exceptions_filtra_por_criticality(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")
    seed_shipments(db_session)

    response = client.get(
        "/api/v1/shipments/exceptions?criticality=alta",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["tracking_code"] == "TRK-ALTA"


def test_exceptions_route_registrada() -> None:
    from app.main import app
    import app.modules.shipments.router as router_module
    assert "exceptions" in open(router_module.__file__, encoding="utf-8").read()
    routes = {getattr(r, "path", "") for r in app.routes}
    assert "/api/v1/shipments/exceptions" in routes
