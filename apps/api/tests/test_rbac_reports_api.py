"""Test RBAC for Reports API endpoints."""


from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_reports_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on reports endpoints."""
    response = client.get("/api/v1/reports/daily")
    assert response.status_code == 401

    response = client.post("/api/v1/reports/daily/generate", json={"report_date": "2025-01-21"})
    assert response.status_code == 401

    response = client.get("/api/v1/reports/daily/1")
    assert response.status_code == 401


def test_reports_generate_without_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without reports:write permission receives 403 on generate."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_reports_admin_can_generate(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin with reports:write can generate report."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_reports_manager_can_generate(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager with reports:write can generate report."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_reports_viewer_can_list(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer with reports:read can list reports."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/reports/daily", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_reports_viewer_cannot_generate(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer cannot generate report (no reports:write)."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_reports_operator_cannot_generate(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator cannot generate report (no reports:write)."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.post(
        "/api/v1/reports/daily/generate",
        json={"report_date": "2025-01-21"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_reports_gestor_can_list(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that gestor with reports:read can list reports."""
    create_user_with_roles(db_session, "gestor@ilex.com", "123456", ["gestor"])
    token = login(client, "gestor@ilex.com", "123456")

    response = client.get("/api/v1/reports/daily", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
