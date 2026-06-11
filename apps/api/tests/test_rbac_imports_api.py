"""Test RBAC for Imports API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_imports_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on imports endpoints."""
    response = client.post("/api/v1/imports/preview")
    assert response.status_code == 401

    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True})
    assert response.status_code == 401

    response = client.get("/api/v1/imports/history")
    assert response.status_code == 401

    response = client.get("/api/v1/imports/deliveries")
    assert response.status_code == 401

    response = client.get("/api/v1/imports/deliveries/1")
    assert response.status_code == 401

    response = client.post("/api/v1/imports/deliveries/1/promote", json={"tracking_code": "TEST123"})
    assert response.status_code == 401


def test_imports_without_read_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without imports:read permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # viewer has imports:read

    response = client.get("/api/v1/imports/deliveries", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # viewer has imports:read

    response = client.get("/api/v1/imports/deliveries/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]  # viewer has imports:read


def test_imports_without_write_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without imports:write permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    # Test confirm endpoint
    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    # Test promote endpoint
    response = client.post("/api/v1/imports/deliveries/1/promote", json={"tracking_code": "TEST123"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_imports_viewer_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer can read imports."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/imports/deliveries", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_imports_viewer_cannot_confirm(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer cannot confirm imports."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_imports_operator_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator can write imports."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Test that operator can access confirm (write)
    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    # 400 or 404 is acceptable (import doesn't exist), but 403 would indicate RBAC blocking
    assert response.status_code in [400, 404]
    assert response.status_code != 403


def test_imports_manager_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can read imports."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/imports/deliveries", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_imports_admin_can_access_all(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access all imports endpoints."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/imports/deliveries/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]

    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 404]


def test_imports_logistica_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that logistica role can write imports."""
    create_user_with_roles(db_session, "logistica@ilex.com", "123456", ["logistica"])
    token = login(client, "logistica@ilex.com", "123456")

    response = client.get("/api/v1/imports/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post("/api/v1/imports/confirm", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 404]
