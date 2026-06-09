import logging

from fastapi import FastAPI, Request

from app.core.errors import register_exception_handlers
from app.modules.auth.router import router as auth_router
from app.modules.carriers.router import router as carriers_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.health.router import router as health_router
from app.modules.shipments.router import router as shipments_router
from app.modules.imports.router import router as imports_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router
from app.modules.sla.router import router as sla_router


def create_app() -> FastAPI:
    app = FastAPI(title="Ilex API", version="1.0.0")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

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
    app.include_router(dashboard_router, prefix="/api/v1")
    app.include_router(health_router)
    return app


app = create_app()
