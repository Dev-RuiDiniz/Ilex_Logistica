import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, settings
from app.core.rate_limit import RateLimiter, RedisRateLimiter, rate_limit_rule
from app.core.errors import register_exception_handlers
from app.modules.auth.router import router as auth_router
from app.modules.audit.router import router as audit_router
from app.modules.carriers.router import router as carriers_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.health.router import router as health_router
from app.modules.shipments.router import router as shipments_router
from app.modules.imports.router import router as imports_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router
from app.modules.sla.router import router as sla_router
from app.modules.alerts.router import router as alerts_router
from app.modules.orders.router import router as orders_router
from app.modules.orders.quotes_router import router as quotes_router


def create_app(app_settings: Settings = settings, rate_limiter: RateLimiter | None = None) -> FastAPI:
    production = app_settings.environment.lower() == "production"
    app = FastAPI(
        title=app_settings.app_name,
        version="1.0.0",
        debug=app_settings.debug,
        docs_url=None if production else "/docs",
        redoc_url=None if production else "/redoc",
        openapi_url=None if production else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    limiter = rate_limiter or (RedisRateLimiter(app_settings.redis_url) if app_settings.redis_url else None)

    @app.middleware("http")
    async def enforce_rate_limit(request: Request, call_next):
        rule = rate_limit_rule(request)
        if rule is None or limiter is None:
            return await call_next(request)
        key, limit = rule
        try:
            decision = await limiter.check(key, limit)
        except Exception:
            if production:
                return JSONResponse(status_code=503, content={"detail": "controle de trafego indisponivel"})
            return await call_next(request)
        if not decision.allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "limite de requisicoes excedido"},
                headers={"Retry-After": str(decision.retry_after)},
            )
        return await call_next(request)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Enable logging middleware unless explicitly disabled for testing
    enable_logging = True
    
    if enable_logging:
        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            logger = logging.getLogger("ilex.api.requests")
            logger.info("request_started method=%s path=%s", request.method, request.url.path)
            response = await call_next(request)
            logger.info(
                "request_finished method=%s path=%s status_code=%s",
                request.method,
                request.url.path,
                response.status_code,
            )
            return response

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    register_exception_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(carriers_router, prefix="/api/v1")
    app.include_router(shipments_router, prefix="/api/v1")
    app.include_router(imports_router, prefix="/api/v1")
    app.include_router(reports_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(sla_router, prefix="/api/v1")
    app.include_router(alerts_router, prefix="/api/v1")
    app.include_router(audit_router, prefix="/api/v1")
    app.include_router(dashboard_router, prefix="/api/v1")
    app.include_router(orders_router, prefix="/api/v1")
    app.include_router(quotes_router, prefix="/api/v1")
    app.include_router(health_router)
    return app


app = create_app()
