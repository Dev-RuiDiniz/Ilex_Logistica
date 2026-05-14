from fastapi.testclient import TestClient
import importlib
from sqlalchemy.exc import OperationalError

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
