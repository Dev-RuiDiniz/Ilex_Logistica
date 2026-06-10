import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import hash_password
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.modules.users.models import Role, User

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def disable_logging_middleware() -> Generator[None, None, None]:
    os.environ["ENABLE_LOGGING_MIDDLEWARE"] = "false"
    yield
    os.environ.pop("ENABLE_LOGGING_MIDDLEWARE", None)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def seed_roles(db_session: Session) -> None:
    for role_name in ["admin", "logistica", "gestor", "auditoria"]:
        db_session.add(Role(name=role_name))
    db_session.commit()


@pytest.fixture
def seed_carrier(db_session: Session):
    """Seed a test carrier for import tests."""
    from app.modules.carriers.models import Carrier
    carrier = Carrier(name="Test Carrier")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    return carrier


def create_user_with_roles(db: Session, email: str, password: str, roles: list[str]) -> User:
    user = User(email=email, full_name=email.split("@")[0], password_hash=hash_password(password), is_active=True)
    db.add(user)
    db.commit()
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        user.roles.append(role)
    db.commit()
    db.refresh(user)
    return user



@pytest.fixture
def seed_braspress_carrier(db_session: Session):
    """Seed a fake Braspress carrier for Braspress import tests."""
    from app.modules.carriers.models import Carrier
    carrier = Carrier(name="Braspress")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    return carrier


def login(client: TestClient, email: str, password: str) -> str:
    """Helper function to login and return access token."""
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(db_session: Session, client: TestClient, seed_roles) -> dict[str, str]:
    create_user_with_roles(db_session, "test@example.com", "test123", ["admin"])
    token = login(client, "test@example.com", "test123")
    return {"Authorization": f"Bearer {token}"}
