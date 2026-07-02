from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_usuario_sem_permissao_recebe_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")

    response = client.post(
        "/api/v1/carriers",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Transportes A", "external_code": "TPA-1", "whatsapp": "+5511999990001", "email": "a@example.com", "integration_metadata": {}},
    )
    assert response.status_code == 403


def test_auditor_consegue_leitura_sem_edicao(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    admin_token = login(client, "admin@ilex.com", "123456")
    client.post(
        "/api/v1/carriers",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Transportes A", "external_code": "TPA-1", "whatsapp": "+5511999990001", "email": "a@example.com", "integration_metadata": {"vendor": "x"}},
    )
    auditor_token = login(client, "audit@ilex.com", "123456")

    list_response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {auditor_token}"})
    edit_response = client.put(
        "/api/v1/carriers/1",
        headers={"Authorization": f"Bearer {auditor_token}"},
        json={"name": "Alterado"},
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert edit_response.status_code == 403


def test_crud_basico_transportadoras(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/carriers",
        headers=headers,
        json={"name": "Transportes B", "external_code": "TPB", "whatsapp": "+5511999990002", "email": "b@example.com", "integration_metadata": {"erp": "totvs"}},
    )
    assert created.status_code == 201

    updated = client.put("/api/v1/carriers/1", headers=headers, json={"external_code": "TPB-2"})
    assert updated.status_code == 200
    assert updated.json()["external_code"] == "TPB-2"

    inactivated = client.post("/api/v1/carriers/1/inactivate", headers=headers)
    assert inactivated.status_code == 200
    assert inactivated.json()["is_active"] is False

    listed = client.get("/api/v1/carriers", headers=headers)
    assert listed.status_code == 200
    assert listed.json() == []


def test_cria_e_atualiza_whatsapp_email(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/carriers",
        headers=headers,
        json={"name": "Transportes C", "external_code": "TPC", "whatsapp": "+5511999990003", "email": "c@example.com"},
    )
    assert created.status_code == 201
    data = created.json()
    assert data["whatsapp"] == "+5511999990003"
    assert data["email"] == "c@example.com"

    updated = client.put(
        "/api/v1/carriers/1",
        headers=headers,
        json={"whatsapp": "+5511988880003", "email": "novo@example.com"},
    )
    assert updated.status_code == 200
    data = updated.json()
    assert data["whatsapp"] == "+5511988880003"
    assert data["email"] == "novo@example.com"


def test_payload_invalido_retorna_422_padronizado(
    client: TestClient, db_session: Session, seed_roles: None
) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")
    response = client.post(
        "/api/v1/carriers",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "A"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
