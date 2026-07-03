import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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


def create_app() -> FastAPI:
    app = FastAPI(title="Ilex API", version="1.0.0")

    cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    extra_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if extra_origins:
        for origin in extra_origins.split(","):
            origin = origin.strip()
            if origin and origin not in cors_origins:
                cors_origins.append(origin)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Enable logging middleware unless explicitly disabled for testing
    enable_logging = os.getenv("ENABLE_LOGGING_MIDDLEWARE", "true").lower() == "true"
    
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
