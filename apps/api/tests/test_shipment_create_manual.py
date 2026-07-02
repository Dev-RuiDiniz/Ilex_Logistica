"""Test creation of a single shipment via POST /api/v1/shipments."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_create_shipment_manual_com_sucesso(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    payload = {
        "tracking_code": "TRK-MANUAL-001",
        "carrier_id": carrier.id,
        "estimated_delivery": "2026-07-10T10:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, São Paulo - SP",
        "destination_address": "Rua B, Rio de Janeiro - RJ",
        "invoice_number": "123456",
        "amount": 1500.50,
        "due_date": "2026-07-15T10:00:00",
    }

    response = client.post("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"}, json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["tracking_code"] == "TRK-MANUAL-001"
    assert body["carrier_id"] == carrier.id
    assert body["status"] == "pending"
    assert body["recipient_name"] == "João Silva"
    assert body["amount"] == 1500.50
    assert body["criticality"] == "normal"

    from app.modules.shipments.models import Shipment

    shipment = db_session.query(Shipment).filter(Shipment.tracking_code == "TRK-MANUAL-001").first()
    assert shipment is not None
    assert shipment.delay_days == 0


def test_create_shipment_manual_sem_permissao_retorna_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post(
        "/api/v1/shipments",
        headers={"Authorization": f"Bearer {token}"},
        json={"tracking_code": "X", "carrier_id": 1, "estimated_delivery": "2026-07-10", "recipient_name": "X", "recipient_phone": "X", "origin_address": "X", "destination_address": "X"},
    )
    assert response.status_code == 403


def test_create_shipment_manual_transportadora_inexistente_retorna_404(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.post(
        "/api/v1/shipments",
        headers={"Authorization": f"Bearer {token}"},
        json={"tracking_code": "TRK-404", "carrier_id": 99999, "estimated_delivery": "2026-07-10", "recipient_name": "X", "recipient_phone": "X", "origin_address": "X", "destination_address": "X"},
    )
    assert response.status_code == 404
