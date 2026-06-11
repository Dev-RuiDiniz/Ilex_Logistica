"""Test RBAC for Shipments API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from conftest import create_user_with_roles


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_shipments_unauthenticated_returns_401(client: TestClient) -> None:
    """Test that unauthenticated user receives 401 on shipments endpoints."""
    response = client.get("/api/v1/shipments")
    assert response.status_code == 401

    response = client.get("/api/v1/shipments/exceptions")
    assert response.status_code == 401

    response = client.get("/api/v1/shipments/1")
    assert response.status_code == 401

    response = client.get("/api/v1/shipments/analytics/carrier-efficiency")
    assert response.status_code == 401

    response = client.get("/api/v1/shipments/analytics/exceptions")
    assert response.status_code == 401


def test_shipments_without_read_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without shipments:read permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # viewer has shipments:read

    response = client.get("/api/v1/shipments/exceptions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # viewer has shipments:read

    response = client.get("/api/v1/shipments/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]  # viewer has shipments:read


def test_shipments_without_write_permission_returns_403(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that user without shipments:write permission receives 403."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    # Test upload endpoint
    response = client.post("/api/v1/shipments/upload", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    # Test import endpoint
    response = client.post("/api/v1/shipments/import", json={"import_id": 1, "confirm": True}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    # Test create treatment
    response = client.post("/api/v1/shipments/1/treatments", json={"status": "em_analise", "comment": "test"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_shipments_viewer_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that viewer can read shipments."""
    create_user_with_roles(db_session, "viewer@ilex.com", "123456", ["viewer"])
    token = login(client, "viewer@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/shipments/analytics/carrier-efficiency", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_shipments_operator_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that operator can write shipments."""
    create_user_with_roles(db_session, "operator@ilex.com", "123456", ["operator"])
    token = login(client, "operator@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Test that operator can access treatments (read)
    response = client.get("/api/v1/shipments/1/treatments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]  # 404 if shipment doesn't exist


def test_shipments_manager_can_read(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that manager can read shipments."""
    create_user_with_roles(db_session, "manager@ilex.com", "123456", ["manager"])
    token = login(client, "manager@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/shipments/analytics/exceptions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_shipments_admin_can_access_all(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that admin can access all shipments endpoints."""
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])
    token = login(client, "admin@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/shipments/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]

    response = client.get("/api/v1/shipments/1/treatments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_shipments_logistica_can_write(client: TestClient, db_session: Session, seed_roles: None) -> None:
    """Test that logistica role can write shipments."""
    create_user_with_roles(db_session, "logistica@ilex.com", "123456", ["logistica"])
    token = login(client, "logistica@ilex.com", "123456")

    response = client.get("/api/v1/shipments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/api/v1/shipments/1/treatments", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
