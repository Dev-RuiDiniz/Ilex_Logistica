"""Test RBAC for Alerts API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_alerts_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on alerts endpoints."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 401

    response = client.get("/api/v1/alerts/summary")
    assert response.status_code == 401

    response = client.post("/api/v1/alerts/generate")
    assert response.status_code == 401

    response = client.patch("/api/v1/alerts/1/read")
    assert response.status_code == 401

    response = client.patch("/api/v1/alerts/1/resolve")
    assert response.status_code == 401


def test_alerts_write_without_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without alerts:write permission receives 403 on write actions."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post("/api/v1/alerts/generate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.patch("/api/v1/alerts/1/read", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.patch("/api/v1/alerts/1/resolve", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_alerts_read_without_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without alerts:read permission receives 403 on read actions."""
    # Create a role without any permissions
    from app.modules.users.models import Role
    from app.core.security import hash_password
    from app.modules.users.models import User

    no_perms_role = Role(name="no_perms")
    db_session.add(no_perms_role)
    db_session.commit()

    user = User(
        email="noperms@ilex.com",
        full_name="No Perms",
        password_hash=hash_password("123456"),
        is_active=True,
    )
    user.roles.append(no_perms_role)
    db_session.add(user)
    db_session.commit()

    token = login(client, "noperms@ilex.com", "123456")

    response = client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.get("/api/v1/alerts/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_alerts_viewer_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer with alerts:read can list and summary."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/alerts/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_alerts_operator_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator with alerts:write can execute write actions."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.post("/api/v1/alerts/generate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_alerts_manager_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager with alerts:write can execute write actions."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.post("/api/v1/alerts/generate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_alerts_admin_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can execute all alert actions."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post("/api/v1/alerts/generate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
