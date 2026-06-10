"""Test RBAC for Users API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_users_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on users endpoints."""
    response = client.get("/api/v1/users")
    assert response.status_code == 401

    response = client.post("/api/v1/users", json={"email": "test@example.com", "password": "123456", "full_name": "Test User", "roles": ["viewer"]})
    assert response.status_code == 401

    response = client.put("/api/v1/users/1", json={"full_name": "Updated User"})
    assert response.status_code == 401

    response = client.post("/api/v1/users/1/inactivate")
    assert response.status_code == 401


def test_users_without_read_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without users:read permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403  # viewer does not have users:read


def test_users_without_write_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without users:write permission receives 403."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.post("/api/v1/users", json={"email": "test@example.com", "password": "123456", "full_name": "Test User", "roles": ["viewer"]}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.put("/api/v1/users/1", json={"full_name": "Updated User"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.post("/api/v1/users/1/inactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_viewer_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer cannot access users."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_operator_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator cannot access users."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_manager_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager cannot access users."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_logistica_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that logistica cannot access users."""
    create_user_with_roles(db_session, "logistica@ilex.com", "123456", ["logistica"])
    token = login(client, "logistica@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_auditoria_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that auditoria cannot access users."""
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_users_admin_can_access_all(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access all users endpoints."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post("/api/v1/users", json={"email": "new@example.com", "password": "123456", "full_name": "New User", "roles": ["viewer"]}, headers={"Authorization": f"Bearer {token}"})
    # 400 is acceptable (validation error), but 403 would indicate RBAC blocking
    assert response.status_code in [201, 400]
    assert response.status_code != 403

    response = client.put("/api/v1/users/1", json={"full_name": "Updated User"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]

    response = client.post("/api/v1/users/1/inactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
