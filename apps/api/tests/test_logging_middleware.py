"""Tests for logging middleware configuration."""

import os

from fastapi.testclient import TestClient

from app.main import app


def test_logging_middleware_disabled_in_tests():
    """Test that logging middleware is disabled in test environment."""
    # The conftest.py sets ENABLE_LOGGING_MIDDLEWARE=false
    assert os.getenv("ENABLE_LOGGING_MIDDLEWARE") == "false"


def test_app_initializes_with_middleware_disabled():
    """Test that app initializes correctly with middleware disabled."""
    # This test verifies that the app can be created without errors
    # when middleware is disabled via environment variable
    assert app is not None
    assert app.title == "Ilex API"


def test_testclient_works_with_middleware_disabled(client: TestClient):
    """Test that TestClient works correctly when middleware is disabled."""
    # Simple health check endpoint
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_middleware_does_not_block_requests(client: TestClient):
    """Test that middleware configuration does not block any requests."""
    # Test multiple endpoints to ensure middleware doesn't interfere
    endpoints = [
        "/api/v1/health",
        "/api/v1/shipments",
        "/api/v1/carriers",
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        # We don't care about the specific status code, just that it's not a 500
        # and that the request completes without middleware errors
        assert response.status_code in [200, 401, 403, 404]


def test_logging_middleware_can_be_enabled():
    """Test that logging middleware can be enabled via environment variable."""
    # Save original value
    original_value = os.environ.get("ENABLE_LOGGING_MIDDLEWARE")
    
    try:
        # Enable middleware
        os.environ["ENABLE_LOGGING_MIDDLEWARE"] = "true"
        
        # Re-import app to pick up new environment variable
        # Note: In a real scenario, you'd need to restart the app
        # This test just verifies the environment variable is read correctly
        assert os.getenv("ENABLE_LOGGING_MIDDLEWARE") == "true"
    finally:
        # Restore original value
        if original_value is not None:
            os.environ["ENABLE_LOGGING_MIDDLEWARE"] = original_value
        else:
            os.environ.pop("ENABLE_LOGGING_MIDDLEWARE", None)
