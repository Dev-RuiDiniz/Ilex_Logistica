from fastapi.testclient import TestClient
import importlib
import os
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from alembic import command
from alembic.config import Config

from app.main import app


def test_a01_health_endpoint_foundation() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_a02_broken_database_ping() -> None:
    session_module = importlib.import_module("app.database.session")

    class BrokenConnection:
        def __enter__(self):
            raise OperationalError("SELECT 1", {}, Exception("boom"))

        def __exit__(self, exc_type, exc, tb):
            return False

    class BrokenEngine:
        def connect(self):
            return BrokenConnection()

    original_engine = session_module.engine
    session_module.engine = BrokenEngine()
    try:
        assert session_module.ping_database() is False
    finally:
        session_module.engine = original_engine


def test_a03_migration_upgrade_downgrade_flow() -> None:
    db_path = Path('migration_test_tdd.db')
    if db_path.exists():
        db_path.unlink()

    cfg = Config('alembic.ini')
    cfg.set_main_option('script_location', 'migrations')
    cfg.set_main_option('sqlalchemy.url', f"sqlite:///{db_path.resolve()}")

    command.upgrade(cfg, 'head')
    engine = create_engine(f"sqlite:///{db_path.resolve()}")
    inspector = inspect(engine)
    assert 'users' in inspector.get_table_names()

    command.downgrade(cfg, 'base')
    inspector = inspect(engine)
    assert 'users' not in inspector.get_table_names()

    engine.dispose()
    os.remove(db_path)
