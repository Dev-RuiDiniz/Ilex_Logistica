from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_list_shipments_paginacao(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar 25 shipments
    for i in range(25):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Testar paginação page 1
    response = client.get(
        "/api/v1/shipments?page=1&page_size=10",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 25
    assert body["page"] == 1
    assert body["page_size"] == 10
    assert len(body["items"]) == 10


def test_list_shipments_filtro_status(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipments com diferentes status
    for i in range(5):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="pending" if i < 3 else "delivered",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por status pending
    response = client.get(
        "/api/v1/shipments?status=pending",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert all(item["status"] == "pending" for item in body["items"])


def test_list_shipments_filtro_carrier_id(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier1 = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportes B", external_code="TPB-1", integration_metadata={})
    db_session.add(carrier1)
    db_session.add(carrier2)
    db_session.flush()

    # Criar shipments para diferentes carriers
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier1.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    
    for i in range(3, 6):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier2.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por carrier_id
    response = client.get(
        f"/api/v1/shipments?carrier_id={carrier1.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert all(item["carrier_id"] == carrier1.id for item in body["items"])


def test_list_shipments_filtro_criticality(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipments com diferentes criticality
    criticalities = ["normal", "normal", "baixa", "media", "alta"]
    for i, crit in enumerate(criticalities):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=i * 10,
            criticality=crit,
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por criticality normal
    response = client.get(
        "/api/v1/shipments?criticality=normal",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all(item["criticality"] == "normal" for item in body["items"])


def test_list_shipments_filtro_tracking_code(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipments
    for i in range(5):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por tracking_code parcial
    response = client.get(
        "/api/v1/shipments?tracking_code=TRK0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert all("TRK0" in item["tracking_code"] for item in body["items"])


def test_list_shipments_filtros_combinados(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier1 = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportes B", external_code="TPB-1", integration_metadata={})
    db_session.add(carrier1)
    db_session.add(carrier2)
    db_session.flush()

    # Criar shipments com diferentes combinações
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier1.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    
    for i in range(3, 6):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier2.id,
            status="delivered",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        )
        db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por status e carrier_id combinados
    response = client.get(
        f"/api/v1/shipments?status=pending&carrier_id={carrier1.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert all(item["status"] == "pending" and item["carrier_id"] == carrier1.id for item in body["items"])
