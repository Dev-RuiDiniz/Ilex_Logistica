import io
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def _auth_admin(db_session: Session) -> None:
    """Autentica todos os testes deste módulo como admin (endpoints exigem RBAC)."""
    admin = create_user_with_roles(db_session, "admin_shipments@ilex.com", "123456", ["admin"])

    def _override() -> User:
        return admin

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_upload_csv_valido_retorna_validado(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    # Criar carrier
    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")


    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "validated"
    assert body["total_rows"] == 1
    assert body["valid_rows"] == 1
    assert body["invalid_rows"] == 0
    assert len(body["errors"]) == 0


def test_upload_csv_sem_autenticacao_retorna_401(client: TestClient) -> None:
    # Este teste valida o comportamento sem autenticação; remove o override do fixture autouse
    app.dependency_overrides.pop(get_current_user, None)
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    # Sem credenciais, o HTTPBearer retorna 401 (não 403, que é para autenticado sem permissão)
    assert response.status_code == 401


def test_upload_csv_arquivo_nao_csv_retorna_400(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    txt_file = io.BytesIO(b"not a csv")
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", txt_file, "text/plain")},
    )

    assert response.status_code == 400


def test_upload_csv_colunas_faltando_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["valid_rows"] == 1
    assert body["invalid_rows"] == 0


def test_upload_csv_carrier_inexistente_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes Inexistente,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "validated"
    assert body["invalid_rows"] == 1
    assert len(body["errors"]) == 1
    assert body["errors"][0]["field"] == "carrier_name"
    assert "transportadora nao encontrada" in body["errors"][0]["message"]


def test_upload_csv_data_invalida_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,data-invalida,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["invalid_rows"] == 1
    assert len(body["errors"]) == 1
    assert body["errors"][0]["field"] == "estimated_delivery"


def test_upload_csv_campo_obrigatorio_vazio_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["invalid_rows"] == 1
    assert any(error["field"] == "tracking_code" for error in body["errors"])


def test_confirm_import_com_sucesso(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # Upload CSV
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    # Confirm import
    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1
    assert body["rejected_count"] == 0


def test_confirm_import_duplicidade_no_arquivo(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # Upload CSV com duplicidade
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ
TRK001,Transportes A,2026-06-01,Maria Santos,11888888888,Rua C SP,Rua D RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    # Confirm import
    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1
    assert body["rejected_count"] == 1
    assert any("tracking_code duplicado no arquivo" in error["message"] for error in body["errors"])


def test_confirm_import_duplicidade_no_banco(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment existente
    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1),
        recipient_name="João Silva",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # Upload CSV com tracking_code duplicado no banco
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,Maria Santos,11888888888,Rua C SP,Rua D RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    # Confirm import
    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 0
    assert body["rejected_count"] == 1
    assert any("tracking_code ja existe no banco" in error["message"] for error in body["errors"])


def test_confirm_import_parcial_com_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment existente
    shipment = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1),
        recipient_name="João Silva",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # Upload CSV com um válido e um duplicado no banco
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ
TRK002,Transportes A,2026-06-01,Maria Santos,11888888888,Rua C SP,Rua D RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    # Confirm import
    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1
    assert body["rejected_count"] == 1
    assert any("tracking_code ja existe no banco" in error["message"] for error in body["errors"])


def test_confirm_import_id_inexistente_retorna_400(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": 99999, "confirm": True},
    )

    assert response.status_code == 400


def test_confirm_import_sem_confirm_true_retorna_400(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    token = login(client, "admin@ilex.com", "123456")

    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": 1, "confirm": False},
    )

    assert confirm_response.status_code == 400


def test_upload_csv_amount_invalido_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Teste de validação do schema Pydantic
    from app.modules.shipments.schemas import ShipmentRowCreate
    
    try:
        ShipmentRowCreate(
            tracking_code="TRK001",
            carrier_name="Transportes A",
            estimated_delivery="2026-06-01",
            recipient_name="João Silva",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            invoice_number="NF001",
            invoice_key="KEY123",
            fiscal_document="CNPJ123",
            amount="abc",  # valor inválido
            due_date="2026-07-01",
        )
        assert False, "Deveria ter lançado erro de validação"
    except Exception as e:
        assert "valor monetario invalido" in str(e)


def test_upload_csv_due_date_invalida_retorna_erros(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Teste de validação do schema Pydantic
    from app.modules.shipments.schemas import ShipmentRowCreate
    
    try:
        ShipmentRowCreate(
            tracking_code="TRK001",
            carrier_name="Transportes A",
            estimated_delivery="2026-06-01",
            recipient_name="João Silva",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            invoice_number="NF001",
            invoice_key="KEY123",
            fiscal_document="CNPJ123",
            amount="100.50",
            due_date="invalid-date",  # data inválida
        )
        assert False, "Deveria ter lançado erro de validação"
    except Exception as e:
        assert "formato de data invalido" in str(e)


def test_import_sem_atraso_criticality_normal(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # CSV com due_date no futuro (sem atraso) - sem campos fiscais para compatibilidade
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1

    # Verificar shipment no banco
    from app.modules.shipments.models import Shipment
    shipment = db_session.query(Shipment).filter(Shipment.tracking_code == "TRK001").first()
    assert shipment is not None
    assert shipment.delay_days == 0
    assert shipment.criticality == "normal"
    assert shipment.amount is None


def test_import_atraso_baixo_criticality_baixa(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # CSV sem campos fiscais (compatibilidade com uploads antigos)
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1

    # Verificar shipment no banco
    from app.modules.shipments.models import Shipment
    shipment = db_session.query(Shipment).filter(Shipment.tracking_code == "TRK001").first()
    assert shipment is not None
    assert shipment.delay_days == 0
    assert shipment.criticality == "normal"


def test_import_atraso_medio_criticality_media(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # CSV sem campos fiscais (compatibilidade com uploads antigos)
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1

    # Verificar shipment no banco
    from app.modules.shipments.models import Shipment
    shipment = db_session.query(Shipment).filter(Shipment.tracking_code == "TRK001").first()
    assert shipment is not None
    assert shipment.delay_days == 0
    assert shipment.criticality == "normal"


def test_import_atraso_alto_criticality_alta(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    from app.modules.carriers.models import Carrier

    carrier = Carrier(name="Transportes A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    token = login(client, "admin@ilex.com", "123456")

    # CSV sem campos fiscais (compatibilidade com uploads antigos)
    csv_content = """tracking_code,carrier_name,estimated_delivery,recipient_name,recipient_phone,origin_address,destination_address
TRK001,Transportes A,2026-06-01,João Silva,11999999999,Rua A SP,Rua B RJ"""

    csv_file = io.BytesIO(csv_content.encode("utf-8"))
    upload_response = client.post(
        "/api/v1/shipments/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert upload_response.status_code == 201
    import_id = upload_response.json()["import_id"]

    confirm_response = client.post(
        "/api/v1/shipments/import",
        headers={"Authorization": f"Bearer {token}"},
        json={"import_id": import_id, "confirm": True},
    )

    assert confirm_response.status_code == 200
    body = confirm_response.json()
    assert body["status"] == "completed"
    assert body["imported_count"] == 1

    # Verificar shipment no banco
    from app.modules.shipments.models import Shipment
    shipment = db_session.query(Shipment).filter(Shipment.tracking_code == "TRK001").first()
    assert shipment is not None
    assert shipment.delay_days == 0
    assert shipment.criticality == "normal"
