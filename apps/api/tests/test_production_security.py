import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.main import create_app
from app.core.rate_limit import RateLimitDecision


def production_settings(**overrides) -> Settings:
    values = {
        "environment": "production",
        "database_url": "postgresql+psycopg2://ilex:strong-password@db:5432/ilex",
        "jwt_secret": "x" * 48,
        "cors_allowed_origins": "https://app.ilex.example",
        "debug": False,
        "redis_url": "redis://redis:6379/0",
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


@pytest.mark.parametrize(
    "overrides",
    [
        {"jwt_secret": "short"},
        {"jwt_secret": "ilex-dev-secret-key-with-at-least-32-bytes"},
        {"database_url": "sqlite:///production.db"},
        {"database_url": "postgresql://ilex:change-me@db/ilex"},
        {"cors_allowed_origins": ""},
        {"cors_allowed_origins": "*"},
        {"cors_allowed_origins": "http://localhost:3000"},
        {"debug": True},
        {"redis_url": None},
    ],
)
def test_production_rejects_insecure_configuration(overrides) -> None:
    with pytest.raises(ValidationError):
        production_settings(**overrides)


def test_security_headers_are_added_and_hsts_is_production_only(client) -> None:
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert "strict-transport-security" not in response.headers

    app = create_app(app_settings=production_settings())
    from fastapi.testclient import TestClient

    with TestClient(app) as production_client:
        production_response = production_client.get("/health")
    assert production_response.headers["strict-transport-security"] == "max-age=31536000; includeSubDomains"


class DenyLimiter:
    async def check(self, key: str, limit: int, window_seconds: int = 60) -> RateLimitDecision:
        return RateLimitDecision(False, 42)


class FailingLimiter:
    async def check(self, key: str, limit: int, window_seconds: int = 60) -> RateLimitDecision:
        raise ConnectionError("redis unavailable")


def test_rate_limit_returns_429_and_retry_after() -> None:
    from fastapi.testclient import TestClient

    with TestClient(create_app(rate_limiter=DenyLimiter())) as limited_client:
        response = limited_client.post("/api/v1/auth/login", json={"email": "fake@example.test", "password": "fake"})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "42"


def test_production_fails_secure_when_redis_is_unavailable() -> None:
    from fastapi.testclient import TestClient

    with TestClient(create_app(app_settings=production_settings(), rate_limiter=FailingLimiter())) as secure_client:
        response = secure_client.post("/api/v1/auth/login", json={"email": "fake@example.test", "password": "fake"})
    assert response.status_code == 503
