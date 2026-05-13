import importlib

import pytest
from sqlalchemy.exc import OperationalError


def test_ping_database_returns_false_when_connection_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    session_module = importlib.import_module("app.database.session")

    class BrokenConnection:
        def __enter__(self):
            raise OperationalError("SELECT 1", {}, Exception("boom"))

        def __exit__(self, exc_type, exc, tb):
            return False

    class BrokenEngine:
        def connect(self):
            return BrokenConnection()

    monkeypatch.setattr(session_module, "engine", BrokenEngine())
    assert session_module.ping_database() is False
