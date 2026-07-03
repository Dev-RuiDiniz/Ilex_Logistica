from dataclasses import dataclass
from typing import Protocol

from fastapi import Request

from app.core.security import decode_token


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    retry_after: int


class RateLimiter(Protocol):
    async def check(self, key: str, limit: int, window_seconds: int = 60) -> RateLimitDecision: ...


class RedisRateLimiter:
    def __init__(self, redis_url: str):
        from redis.asyncio import from_url

        self.client = from_url(redis_url, encoding="utf-8", decode_responses=True)

    async def check(self, key: str, limit: int, window_seconds: int = 60) -> RateLimitDecision:
        redis_key = f"ilex:rate:{key}"
        async with self.client.pipeline(transaction=True) as pipeline:
            pipeline.incr(redis_key)
            pipeline.ttl(redis_key)
            count, ttl = await pipeline.execute()
        if count == 1 or ttl < 0:
            await self.client.expire(redis_key, window_seconds)
            ttl = window_seconds
        return RateLimitDecision(allowed=count <= limit, retry_after=max(int(ttl), 1))


def rate_limit_rule(request: Request) -> tuple[str, int] | None:
    path = request.url.path
    if not path.startswith("/api/v1") or path in {"/api/v1/health", "/api/v1/health/live", "/api/v1/health/ready"}:
        return None
    if path == "/api/v1/auth/login":
        return (f"login:{_client_ip(request)}", 5)
    if path == "/api/v1/auth/refresh":
        return (f"refresh:{_client_ip(request)}", 10)
    identity = _subject(request) or _client_ip(request)
    if "/imports" in path or "/quote-rounds" in path:
        return (f"operation:{identity}", 30)
    return (f"private:{identity}", 120)


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _subject(request: Request) -> str | None:
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    try:
        return str(decode_token(header.split(" ", 1)[1]).get("sub"))
    except Exception:
        return None
