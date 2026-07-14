# LOG-021: Testes Red para promoção Delivery → Shipment

import pytest
<<<<<<< HEAD


@pytest.fixture(autouse=True)
def authenticated_requests(client, auth_headers):
    client.headers.update(auth_headers)
=======
from sqlalchemy.orm import Session

from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from conftest import create_user_with_roles


@pytest.fixture(autouse=True)
def _auth_admin(db_session: Session) -> None:
    """Autentica todos os testes deste módulo como admin (endpoints exigem RBAC)."""
    admin = create_user_with_roles(db_session, "admin_promote@ilex.com", "123456", ["admin"])

    def _override() -> User:
        return admin

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)
>>>>>>> fix/infra-setup-local


def test_promote_delivery_cria_shipment_com_payload_completo(client, db_session) -> None:
    """Promove Delivery existente com payload completo e cria Shipment."""
    # Criar Carrier
    from app.modules.carriers.models import Carrier
    
    carrier = Carrier(
        name="TRANSPORTADORA_TESTE",
        external_code="TRANSP_TESTE"
    )
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    
    # Criar Delivery
    from app.modules.imports.models import Delivery
    from datetime import date
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    # Payload de promoção
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": carrier.id,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456",
        "shipment_status": "pending"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["tracking_code"] == "TRACK123"
    assert body["recipient_name"] == "João Silva"


def test_promote_delivery_inexistente_retorna_404(client) -> None:
    """Retorna 404 para Delivery inexistente."""
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": 1,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post("/api/v1/imports/deliveries/99999/promote", json=payload)
    assert response.status_code == 404
    assert "entrega" in response.json()["detail"].lower()


def test_promote_delivery_rejeita_payload_sem_campo_obrigatorio(client, db_session) -> None:
    """Rejeita payload sem campo obrigatório."""
    from app.modules.imports.models import Delivery
    from datetime import date
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    # Payload sem tracking_code (obrigatório)
    payload = {
        "carrier_id": 1,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 422


def test_promote_delivery_rejeita_carrier_inexistente(client, db_session) -> None:
    """Rejeita carrier inexistente."""
    # Criar Carrier válido
    from app.modules.carriers.models import Carrier
    
    carrier = Carrier(
        name="TRANSPORTADORA_TESTE",
        external_code="TRANSP_TESTE"
    )
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    
    # Criar Delivery
    from app.modules.imports.models import Delivery
    from datetime import date
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": 99999,  # Carrier inexistente
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 404
    assert "carrier" in response.json()["detail"].lower()


def test_promote_delivery_impede_duplicidade_por_tracking_code(client, db_session) -> None:
    """Impede duplicidade por tracking_code."""
    # Criar Carrier
    from app.modules.carriers.models import Carrier
    
    carrier = Carrier(
        name="TRANSPORTADORA_TESTE",
        external_code="TRANSP_TESTE"
    )
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    
    # Criar Delivery
    from app.modules.imports.models import Delivery
    from app.modules.shipments.models import Shipment
    from datetime import date, datetime
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    # Criar Shipment com tracking_code já existente
    shipment = Shipment(
        tracking_code="TRACK123",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime(2026, 5, 20),
        recipient_name="Maria Santos",
        recipient_phone="11988888888",
        origin_address="Rua C, 789",
        destination_address="Rua D, 012"
    )
    db_session.add(shipment)
    db_session.commit()
    
    payload = {
        "tracking_code": "TRACK123",  # Já existe
        "carrier_id": carrier.id,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 409
    assert "tracking_code" in response.json()["detail"].lower()


def test_promote_delivery_preserva_delivery_original(client, db_session) -> None:
    """Preserva Delivery original após promoção."""
    # Criar Carrier
    from app.modules.carriers.models import Carrier
    
    carrier = Carrier(
        name="TRANSPORTADORA_TESTE",
        external_code="TRANSP_TESTE"
    )
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    
    # Criar Delivery
    from app.modules.imports.models import Delivery
    from datetime import date
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    original_nf = delivery.nf
    original_transportadora = delivery.transportadora
    
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": carrier.id,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 201
    
    # Verificar que Delivery original foi preservado
    db_session.refresh(delivery)
    assert delivery.nf == original_nf
    assert delivery.transportadora == original_transportadora


def test_promote_delivery_exige_autenticacao(client) -> None:
    client.headers.pop("Authorization", None)
    """Exige autenticação."""
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": 1,
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post("/api/v1/imports/deliveries/1/promote", json=payload)
    assert response.status_code == 401


def test_promote_delivery_resposta_nao_expoe_stack_trace(client, db_session) -> None:
    """Não expõe stack trace em erro."""
    from app.modules.imports.models import Delivery
    from datetime import date
    
    delivery = Delivery(
        nf="NF123",
        transportadora="TRANSPORTADORA_TESTE",
        data_coleta=date(2026, 5, 14),
        valor_frete=10.50,
        percentual_frete=5.00
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    
    payload = {
        "tracking_code": "TRACK123",
        "carrier_id": 99999,  # Carrier inexistente para causar erro
        "estimated_delivery": "2026-05-20T00:00:00",
        "recipient_name": "João Silva",
        "recipient_phone": "11999999999",
        "origin_address": "Rua A, 123",
        "destination_address": "Rua B, 456"
    }
    
    response = client.post(f"/api/v1/imports/deliveries/{delivery.id}/promote", json=payload)
    assert response.status_code == 404
    body = response.json()
    assert "Traceback" not in str(body)
    assert 'File "' not in str(body)
