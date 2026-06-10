"""Test RBAC for Audit API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_audit_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on audit endpoints."""
    response = client.get("/api/v1/audit")
    assert response.status_code == 401

    response = client.get("/api/v1/audit/summary")
    assert response.status_code == 401

    response = client.get("/api/v1/audit/1")
    assert response.status_code == 401


def test_audit_without_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without audit:read permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.get("/api/v1/audit/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    response = client.get("/api/v1/audit/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_audit_operator_cannot_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator cannot access audit logs."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_audit_manager_can_access_logs(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can access audit logs."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_audit_manager_can_access_summary(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can access audit summary."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/audit/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_audit_admin_can_access_detail(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access audit log detail."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/audit/1", headers={"Authorization": f"Bearer {token}"})
    # 404 is acceptable (log doesn't exist), but 403 would indicate RBAC blocking
    assert response.status_code in [200, 404]
    assert response.status_code != 403


def test_audit_auditoria_can_access(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that auditoria role can access audit logs."""
    create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    token = login(client, "audit@ilex.com", "123456")

    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
