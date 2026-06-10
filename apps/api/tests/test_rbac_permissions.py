"""Test RBAC permissions for BETA-020A."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_unauthenticated_user_receives_401_on_protected_endpoints(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on protected endpoints."""
    # Test audit logs endpoint
    response = client.get("/api/v1/audit")
    assert response.status_code == 401

    # Test reports endpoint
    response = client.get("/api/v1/reports/daily")
    assert response.status_code == 401

    # Test alerts endpoint
    response = client.get("/api/v1/alerts")
    assert response.status_code == 401

    # Test SLA rules endpoint
    response = client.get("/api/v1/sla/rules")
    assert response.status_code == 401


def test_user_without_permission_receives_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    # Try to access audit logs (requires audit:read)
    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    # Try to generate report (requires reports:write)
    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_access_all_endpoints(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access all endpoints."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    # Audit logs
    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Reports
    response = client.get("/api/v1/reports/daily", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Alerts
    response = client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # SLA rules
    response = client.get("/api/v1/sla/rules", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_manager_can_access_audit_reports_alerts_sla(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can access audit, reports, alerts, and SLA."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    # Audit logs
    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Reports
    response = client.get("/api/v1/reports/daily", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Alerts
    response = client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # SLA rules
    response = client.get("/api/v1/sla/rules", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_operator_cannot_access_audit(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator cannot access audit logs."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    # Try to access audit logs
    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_viewer_can_read_but_not_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer can read but not write."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    # Can read reports
    response = client.get("/api/v1/reports/daily", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Cannot write reports
    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403

    # Cannot write alerts
    response = client.post(
        "/api/v1/alerts/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_unknown_role_fails_safely(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that unknown role fails safely."""
    # Create user with unknown role
    from app.modules.users.models import User, Role
    from app.core.security import hash_password

    unknown_role = Role(name="unknown_role")
    db_session.add(unknown_role)
    db_session.commit()

    user = User(
        email="unknown@ilex.com",
        full_name="Unknown User",
        password_hash=hash_password("123456"),
        is_active=True,
    )
    user.roles.append(unknown_role)
    db_session.add(user)
    db_session.commit()

    token = login(client, "unknown@ilex.com", "123456")

    # Should fail with 403 on protected endpoints
    response = client.get("/api/v1/audit", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_public_endpoints_still_work(client: TestClient) -> None:
    """Test that public endpoints still work (if any)."""
    # Health check should be public
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    # Login should be public
    response = client.post("/api/v1/auth/login", json={"email": "test@test.com", "password": "wrong"})
    assert response.status_code == 401  # Wrong password, but endpoint is accessible
