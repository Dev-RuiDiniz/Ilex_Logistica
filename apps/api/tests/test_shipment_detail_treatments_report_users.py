from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()


def seed_base_data(db_session: Session) -> int:
    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()
    shipment = Shipment(
        tracking_code="TRK-DETAIL-1",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC) - timedelta(days=4),
        recipient_name="Cliente A",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        invoice_number="NF123",
        fiscal_document="DOC123",
        amount=150.25,
        due_date=datetime.now(UTC) - timedelta(days=2),
        delay_days=2,
        criticality="baixa",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    return shipment.id


def test_w07_get_shipment_detail(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")["access_token"]
    shipment_id = seed_base_data(db_session)

    response = client.get(f"/api/v1/shipments/{shipment_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == shipment_id
    assert body["tracking_code"] == "TRK-DETAIL-1"
    assert body["criticality"] == "baixa"


def test_w07_get_shipment_detail_404(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")["access_token"]

    response = client.get("/api/v1/shipments/9999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_w11_create_and_list_treatments(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")["access_token"]
    shipment_id = seed_base_data(db_session)

    create_response = client.post(
        f"/api/v1/shipments/{shipment_id}/treatments",
        json={"status": "em_tratativa", "comment": "Contato com transportadora"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 201

    list_response = client.get(
        f"/api/v1/shipments/{shipment_id}/treatments",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["status"] == "em_tratativa"


def test_w11_treatment_write_blocked_for_auditoria(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")["access_token"]
    shipment_id = seed_base_data(db_session)

    response = client.post(
        f"/api/v1/shipments/{shipment_id}/treatments",
        json={"status": "em_tratativa", "comment": "Teste"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_w10_daily_report(client: TestClient, db_session: Session, seed_roles: None) -> None:
    import json

    create_user_with_roles(db_session, "gestor@ilex.com", "123456", ["gestor"])
    token = login(client, "gestor@ilex.com", "123456")["access_token"]
    shipment_id = seed_base_data(db_session)

    # Gerar relatório diário primeiro
    report_date = datetime.now(UTC).date()
    generate_response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": report_date.isoformat()},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert generate_response.status_code == 200

    # Buscar relatório por data
    response = client.get(
        f"/api/v1/reports/daily/by-date/{report_date.isoformat()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    # O summary está em summary_json como string JSON
    summary = json.loads(body["summary_json"])
    assert summary["total_shipments"] >= 1


def test_w15_users_crud_and_roles(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")["access_token"]

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "logistica@ilex.com",
            "full_name": "Operador Logistica",
            "password": "123456",
            "roles": ["logistica"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 201, create_response.text
    created = create_response.json()
    assert created["email"] == "logistica@ilex.com"
    assert "logistica" in created["roles"]

    list_response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert list_response.status_code == 200
    assert any(item["email"] == "logistica@ilex.com" for item in list_response.json())

    update_response = client.put(
        f"/api/v1/users/{created['id']}",
        json={"full_name": "Operador Atualizado", "roles": ["gestor"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["full_name"] == "Operador Atualizado"
    assert "gestor" in updated["roles"]

    inactivate_response = client.post(
        f"/api/v1/users/{created['id']}/inactivate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert inactivate_response.status_code == 200
    assert inactivate_response.json()["is_active"] is False


def test_w15_login_returns_roles_from_backend(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "gestor@ilex.com", "123456", ["gestor"])
    tokens = login(client, "gestor@ilex.com", "123456")
    assert tokens["roles"] == ["gestor"]
