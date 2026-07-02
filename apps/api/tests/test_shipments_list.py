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


# =============================================================================
# P1.2 — Busca, filtros combinados, ordenação e validação (LOG-028/032/033)
# =============================================================================


def test_list_shipments_search_multicampo(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Busca global (search) deve retornar resultados de NF, cliente, rastreio e UF."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipments = [
        Shipment(
            tracking_code="TRK-ALPHA-001",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name="Cliente Alpha",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            invoice_number="NF-ALPHA-001",
            customer_name="Cliente Alpha",
            destination_uf="SP",
        ),
        Shipment(
            tracking_code="TRK-BETA-002",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name="Cliente Beta",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            invoice_number="NF-BETA-002",
            customer_name="Cliente Beta",
            destination_uf="RJ",
        ),
        Shipment(
            tracking_code="TRK-GAMMA-003",
            carrier_id=carrier.id,
            status="delivered",
            estimated_delivery=datetime.now(UTC),
            recipient_name="Cliente Gamma",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B MG",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            invoice_number="NF-GAMMA-003",
            customer_name="Cliente Gamma",
            destination_uf="MG",
        ),
    ]
    for s in shipments:
        db_session.add(s)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Buscar por "ALPHA" — deve encontrar no tracking_code, invoice_number e customer_name
    response = client.get(
        "/api/v1/shipments?search=ALPHA",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["tracking_code"] == "TRK-ALPHA-001"

    # Buscar por "SP" — deve encontrar no destination_uf
    response = client.get(
        "/api/v1/shipments?search=SP",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["destination_uf"] == "SP"


def test_list_shipments_filtro_customer_name(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Filtro por customer_name deve usar ilike (parcial, case-insensitive)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    for i, name in enumerate(["Empresa Alpha Ltda", "Empresa Beta S/A", "Comercio Gamma"]):
        db_session.add(Shipment(
            tracking_code=f"TRK-CN-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Destinatario {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            customer_name=name,
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?customer_name=empresa",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all("empresa" in item["customer_name"].lower() for item in body["items"])


def test_list_shipments_filtro_destination_uf(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Filtro por destination_uf deve ser exato."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    for i, uf in enumerate(["SP", "SP", "RJ", "MG"]):
        db_session.add(Shipment(
            tracking_code=f"TRK-UF-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            destination_uf=uf,
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?destination_uf=SP",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all(item["destination_uf"] == "SP" for item in body["items"])


def test_list_shipments_filtro_month_year(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Filtro por month + year deve combinar corretamente."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    dates = [
        datetime(2026, 1, 15, tzinfo=UTC),
        datetime(2026, 3, 10, tzinfo=UTC),
        datetime(2026, 3, 20, tzinfo=UTC),
        datetime(2026, 6, 5, tzinfo=UTC),
    ]
    for i, dt in enumerate(dates):
        db_session.add(Shipment(
            tracking_code=f"TRK-MY-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=dt,
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?month=3&year=2026",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2


def test_list_shipments_filtros_combinados_3plus(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Combinação de 3+ filtros (status + carrier + UF + mês) sem divergência."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier1 = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportes B", external_code="TPB-1", integration_metadata={})
    db_session.add(carrier1)
    db_session.add(carrier2)
    db_session.flush()

    # 2 shipments que match: carrier1 + pending + SP + março/2026
    for i in range(2):
        db_session.add(Shipment(
            tracking_code=f"TRK-C1-{i:03d}",
            carrier_id=carrier1.id,
            status="pending",
            estimated_delivery=datetime(2026, 3, 15, tzinfo=UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            destination_uf="SP",
        ))

    # 1 shipment que não match (carrier2)
    db_session.add(Shipment(
        tracking_code="TRK-C2-000",
        carrier_id=carrier2.id,
        status="pending",
        estimated_delivery=datetime(2026, 3, 15, tzinfo=UTC),
        recipient_name="Cliente X",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        destination_uf="SP",
    ))

    # 1 shipment que não match (status delivered)
    db_session.add(Shipment(
        tracking_code="TRK-C1-099",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=datetime(2026, 3, 15, tzinfo=UTC),
        recipient_name="Cliente Y",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        destination_uf="SP",
    ))

    # 1 shipment que não match (UF=RJ)
    db_session.add(Shipment(
        tracking_code="TRK-C1-098",
        carrier_id=carrier1.id,
        status="pending",
        estimated_delivery=datetime(2026, 3, 15, tzinfo=UTC),
        recipient_name="Cliente Z",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        destination_uf="RJ",
    ))

    # 1 shipment que não match (mês=6)
    db_session.add(Shipment(
        tracking_code="TRK-C1-097",
        carrier_id=carrier1.id,
        status="pending",
        estimated_delivery=datetime(2026, 6, 15, tzinfo=UTC),
        recipient_name="Cliente W",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        destination_uf="SP",
    ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        f"/api/v1/shipments?status=pending&carrier_id={carrier1.id}&destination_uf=SP&month=3&year=2026",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all(
        item["status"] == "pending"
        and item["carrier_id"] == carrier1.id
        and item["destination_uf"] == "SP"
        for item in body["items"]
    )


def test_list_shipments_sort_by_created_at_asc(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Ordenação ascendente por created_at deve retornar do mais antigo ao mais novo."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    for i in range(5):
        db_session.add(Shipment(
            tracking_code=f"TRK-SORT-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?sort_by=created_at&sort_order=asc",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    dates = [item["created_at"] for item in body["items"]]
    assert dates == sorted(dates)


def test_list_shipments_sort_by_estimated_delivery_desc(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Ordenação descendente por estimated_delivery deve retornar do mais novo ao mais antigo."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    dates = [
        datetime(2026, 1, 15, tzinfo=UTC),
        datetime(2026, 6, 10, tzinfo=UTC),
        datetime(2026, 3, 20, tzinfo=UTC),
    ]
    for i, dt in enumerate(dates):
        db_session.add(Shipment(
            tracking_code=f"TRK-ED-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=dt,
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?sort_by=estimated_delivery&sort_order=desc",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    ed_dates = [item["estimated_delivery"] for item in body["items"]]
    assert ed_dates == sorted(ed_dates, reverse=True)


def test_list_shipments_sort_by_amount(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Ordenação por amount deve funcionar corretamente."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    amounts = [100.00, 50.00, 200.00, 75.00]
    for i, amt in enumerate(amounts):
        db_session.add(Shipment(
            tracking_code=f"TRK-AM-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            amount=amt,
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?sort_by=amount&sort_order=asc",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    amts = [item["amount"] for item in body["items"]]
    assert amts == sorted(amts)


def test_list_shipments_filtro_invoice_number(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Filtro por invoice_number deve usar ilike (parcial)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    for i, nf in enumerate(["NF-001-A", "NF-001-B", "NF-002-C"]):
        db_session.add(Shipment(
            tracking_code=f"TRK-NF-{i:03d}",
            carrier_id=carrier.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            invoice_number=nf,
        ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?invoice_number=NF-001",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all("NF-001" in item["invoice_number"] for item in body["items"])


def test_list_shipments_filtro_invalido_month_13(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """month=13 deve retornar erro de validação 422."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?month=13",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_list_shipments_page_zero_retorna_422(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """page=0 deve retornar erro de validação 422 (ge=1)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?page=0",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_list_shipments_combinacao_fiscal_operacional(
    client: TestClient, db_session: Session, seed_roles: None
) -> None:
    """Combinação de filtros fiscais e operacionais (freight_value_min + status + carrier)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier1 = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportes B", external_code="TPB-1", integration_metadata={})
    db_session.add(carrier1)
    db_session.add(carrier2)
    db_session.flush()

    # 2 que match: carrier1 + pending + freight >= 100
    for i in range(2):
        db_session.add(Shipment(
            tracking_code=f"TRK-FO-{i:03d}",
            carrier_id=carrier1.id,
            status="pending",
            estimated_delivery=datetime.now(UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
            delay_days=0,
            criticality="normal",
            freight_value=150.00,
        ))

    # 1 que não match (freight < 100)
    db_session.add(Shipment(
        tracking_code="TRK-FO-098",
        carrier_id=carrier1.id,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente X",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        freight_value=50.00,
    ))

    # 1 que não match (carrier2)
    db_session.add(Shipment(
        tracking_code="TRK-FO-097",
        carrier_id=carrier2.id,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente Y",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        freight_value=200.00,
    ))

    # 1 que não match (status=delivered)
    db_session.add(Shipment(
        tracking_code="TRK-FO-096",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente Z",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        freight_value=300.00,
    ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        f"/api/v1/shipments?freight_value_min=100&status=pending&carrier_id={carrier1.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all(
        item["status"] == "pending"
        and item["carrier_id"] == carrier1.id
        and item["freight_value"] >= 100
        for item in body["items"]
    )


def test_list_shipments_search_sem_resultado(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Search por termo inexistente deve retornar total=0 e lista vazia."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    db_session.add(Shipment(
        tracking_code="TRK-NOPE-001",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        meta_data="{}",
        is_active=True,
        delay_days=0,
        criticality="normal",
        customer_name="Cliente Teste",
        destination_uf="SP",
    ))
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?search=ZZZINEXISTENTE",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []
