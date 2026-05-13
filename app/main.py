from fastapi import FastAPI

from app.core.errors import register_exception_handlers
from app.modules.auth.router import router as auth_router
from app.modules.carriers.router import router as carriers_router
from app.modules.health.router import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="Ilex API", version="1.0.0")
    register_exception_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(carriers_router, prefix="/api/v1")
    app.include_router(health_router)
    return app


app = create_app()
