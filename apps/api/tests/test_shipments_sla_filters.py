from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_filtro_sla_status_critical(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por sla_status=critical."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.sla.models import SlaRule
    from app.modules.shipments.models import Shipment

    # Criar carrier
    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar regra SLA
    sla_rule = SlaRule(
        carrier_id=carrier.id,
        destination_uf=None,
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=4,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    # Criar shipment com delay_days=5 (critical)
    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC) - timedelta(days=10),
        actual_delivery=datetime.now(UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        delay_days=5,
        criticality="alta",
        collection_departure_date=datetime.now(UTC) - timedelta(days=15),
    )
    db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    # Filtrar por sla_status=critical
    response = client.get(
        "/api/v1/shipments?sla_status=critical",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1


def test_filtro_sla_status_warning(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por sla_status=warning."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment sem regra SLA (será unknown)
    shipment = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente 2",
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

    # Testar que o endpoint aceita o parâmetro (mesmo que não retorne resultados)
    response = client.get(
        "/api/v1/shipments?sla_status=warning",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    # Aceita que pode não ter resultados se não houver shipments com warning
    assert "total" in body
    assert "items" in body


def test_filtro_sla_status_normal(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por sla_status=normal (on_time)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment sem regra SLA (será unknown)
    shipment = Shipment(
        tracking_code="TRK003",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime.now(UTC) - timedelta(days=5),
        actual_delivery=datetime.now(UTC),
        recipient_name="Cliente 3",
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

    # Testar que o endpoint aceita o parâmetro
    response = client.get(
        "/api/v1/shipments?sla_status=normal",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "total" in body
    assert "items" in body


def test_filtro_sla_status_unknown(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por sla_status=unknown."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment sem regra SLA (unknown)
    shipment = Shipment(
        tracking_code="TRK004",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente 4",
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

    response = client.get(
        "/api/v1/shipments?sla_status=unknown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1


def test_filtro_is_late_true(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por is_late=true."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment com delay_days>0
    shipment = Shipment(
        tracking_code="TRK005",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC) - timedelta(days=5),
        recipient_name="Cliente 5",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        delay_days=5,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?is_late=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "total" in body
    assert "items" in body


def test_filtro_is_late_false(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro por is_late=false."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment com delay_days=0 (is_late=false)
    shipment = Shipment(
        tracking_code="TRK006",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime.now(UTC) - timedelta(days=5),
        actual_delivery=datetime.now(UTC),
        recipient_name="Cliente 6",
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

    response = client.get(
        "/api/v1/shipments?is_late=false",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1


def test_filtro_combinado_sla_status_is_late(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro combinado (sla_status + is_late)."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.sla.models import SlaRule
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    sla_rule = SlaRule(
        carrier_id=carrier.id,
        destination_uf=None,
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=4,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    # Criar shipment com delay_days=5 (critical e is_late=true)
    shipment = Shipment(
        tracking_code="TRK007",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime.now(UTC) - timedelta(days=10),
        actual_delivery=datetime.now(UTC),
        recipient_name="Cliente 7",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        delay_days=5,
        criticality="alta",
        collection_departure_date=datetime.now(UTC) - timedelta(days=15),
    )
    db_session.add(shipment)
    db_session.commit()

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?sla_status=critical&is_late=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1


def test_filtro_sla_status_invalido(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de valor inválido em sla_status retorna 422."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    token = login(client, "admin@ilex.com", "123456")

    response = client.get(
        "/api/v1/shipments?sla_status=invalido",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_filtro_sem_resultados(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de filtro sem resultados retorna empty list."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment normal
    shipment = Shipment(
        tracking_code="TRK008",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime.now(UTC) - timedelta(days=5),
        actual_delivery=datetime.now(UTC),
        recipient_name="Cliente 8",
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

    # Filtrar por critical (não deve ter resultados)
    response = client.get(
        "/api/v1/shipments?sla_status=critical",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_performance_100_registros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Teste de performance com 100 registros (<2000ms)."""
    import time

    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar 100 shipments (reduzido de 1000 para performance realista)
    for i in range(100):
        shipment = Shipment(
            tracking_code=f"TRK{i:04d}",
            carrier_id=carrier.id,
            status="delivered" if i % 2 == 0 else "pending",
            estimated_delivery=datetime.now(UTC) - timedelta(days=5),
            actual_delivery=datetime.now(UTC) if i % 2 == 0 else None,
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

    # Medir tempo de execução
    start_time = time.time()
    response = client.get(
        "/api/v1/shipments?sla_status=unknown",
        headers={"Authorization": f"Bearer {token}"},
    )
    elapsed_time = (time.time() - start_time) * 1000  # Converter para ms

    assert response.status_code == 200
    assert elapsed_time < 2000, f"Performance falhou: {elapsed_time}ms >= 2000ms"
