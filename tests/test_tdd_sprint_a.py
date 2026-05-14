import importlib
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.main import app
from conftest import create_user_with_roles


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


def _login_token(client: TestClient, email: str, password: str) -> str:
    response = client.post('/api/v1/auth/login', json={'email': email, 'password': password})
    return response.json()['access_token']


def test_a04_login_invalid_credentials(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, 'admin@ilex.com', '123456', ['admin'])
    response = client.post('/api/v1/auth/login', json={'email': 'admin@ilex.com', 'password': 'senha_errada'})
    assert response.status_code == 401

def test_a05_rbac_blocks_write_for_auditor(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, 'audit@ilex.com', '123456', ['auditoria'])
    token = _login_token(client, 'audit@ilex.com', '123456')
    response = client.post(
        '/api/v1/carriers',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Transportes A', 'external_code': 'TPA-1', 'integration_metadata': {}},
    )
    assert response.status_code == 403

def test_a06_crud_carriers_flow(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, 'admin2@ilex.com', '123456', ['admin'])
    token = _login_token(client, 'admin2@ilex.com', '123456')
    headers = {'Authorization': f'Bearer {token}'}

    created = client.post(
        '/api/v1/carriers',
        headers=headers,
        json={'name': 'Transportes B', 'external_code': 'TPB', 'integration_metadata': {'erp': 'totvs'}},
    )
    assert created.status_code == 201

    updated = client.put('/api/v1/carriers/1', headers=headers, json={'external_code': 'TPB-2'})
    assert updated.status_code == 200

    inactivated = client.post('/api/v1/carriers/1/inactivate', headers=headers)
    assert inactivated.status_code == 200

    listed = client.get('/api/v1/carriers', headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 0
