import pytest
from datetime import UTC, datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment


def test_analytics_endpoint_retorna_200_com_autenticacao(client: TestClient, db_session: Session, seed_roles):
    """Endpoint retorna 200 para usuário com autenticação."""
    # Criar usuário
    from tests.conftest import create_user_with_roles
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    # Login
    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "123456"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Chamar endpoint
    response = client.get(
        "/api/v1/shipments/analytics/carrier-efficiency",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_analytics_endpoint_retorna_payload_esperado(client: TestClient, db_session: Session, seed_roles):
    """Endpoint retorna payload esperado."""
    from tests.conftest import create_user_with_roles
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "123456"})
    token = response.json()["access_token"]

    response = client.get(
        "/api/v1/shipments/analytics/carrier-efficiency",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "carriers" in data
    assert "generated_at" in data
    assert isinstance(data["carriers"], list)


def test_analytics_endpoint_aplica_query_params(client: TestClient, db_session: Session, seed_roles):
    """Endpoint aplica query params."""
    from tests.conftest import create_user_with_roles
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "123456"})
    token = response.json()["access_token"]

    response = client.get(
        "/api/v1/shipments/analytics/carrier-efficiency?month=1&year=2025",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_analytics_nao_conflita_com_rota_dinamica(client: TestClient, db_session: Session, seed_roles):
    """GET /shipments/analytics/carrier-efficiency não deve conflitar com /shipments/{id}."""
    from tests.conftest import create_user_with_roles
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "123456"})
    token = response.json()["access_token"]

    # Rota analytics deve funcionar
    response = client.get(
        "/api/v1/shipments/analytics/carrier-efficiency",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Rota dinâmica deve continuar funcionando
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    response = client.get(
        f"/api/v1/shipments/{shipment.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
