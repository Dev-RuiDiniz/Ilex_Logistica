import socket
from urllib.parse import urlparse

from fastapi import APIRouter, Response, status

from app.core.config import settings
from app.database.session import ping_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready")
def readiness(response: Response) -> dict[str, str | bool]:
    postgresql = ping_database()
    redis = ping_redis(settings.redis_url)
    ready = postgresql and redis
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if ready else "not_ready", "postgresql": postgresql, "redis": redis}


def ping_redis(redis_url: str | None) -> bool:
    if not redis_url:
        return True
    parsed = urlparse(redis_url)
    try:
        with socket.create_connection((parsed.hostname or "localhost", parsed.port or 6379), timeout=1):
            return True
    except OSError:
        return False
