"""Test RBAC for Carriers API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_carriers_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on carriers endpoints."""
    response = client.get("/api/v1/carriers")
    assert response.status_code == 401

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"})
    assert response.status_code == 401

    response = client.put("/api/v1/carriers/1", json={"name": "Updated Carrier"})
    assert response.status_code == 401

    response = client.post("/api/v1/carriers/1/inactivate")
    assert response.status_code == 401


def test_carriers_without_read_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without carriers:read permission receives 403."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403  # operator does not have carriers:read


def test_carriers_without_write_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without carriers:write permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.put("/api/v1/carriers/1", json={"name": "Updated Carrier"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.post("/api/v1/carriers/1/inactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_carriers_viewer_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer can read carriers."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_carriers_viewer_cannot_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer cannot write carriers."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_carriers_operator_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator cannot access carriers."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_carriers_manager_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can read carriers."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_carriers_manager_cannot_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager cannot write carriers."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_carriers_logistica_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that logistica role can write carriers."""
    create_user_with_roles(db_session, "logistica@ilex.com", "123456", ["logistica"])
    token = login(client, "logistica@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"}, headers={"Authorization": f"Bearer {token}"})
    # 409 is acceptable (carrier already exists), but 403 would indicate RBAC blocking
    assert response.status_code in [201, 409]
    assert response.status_code != 403


def test_carriers_auditoria_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that auditoria role can read carriers."""
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_carriers_admin_can_access_all(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access all carriers endpoints."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post("/api/v1/carriers", json={"name": "Test Carrier", "cnpj": "12345678901234"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [201, 409]

    response = client.put("/api/v1/carriers/1", json={"name": "Updated Carrier"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
