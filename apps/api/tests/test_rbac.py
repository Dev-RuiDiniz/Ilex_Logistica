from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_usuario_sem_perfil_escrita_recebe_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")

    response = client.post(
        "/api/v1/carriers",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Transportes A", "external_code": "TPA-1", "integration_metadata": {}},
    )
    assert response.status_code == 403
