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

# Disable logging middleware for tests to avoid TestClient compatibility issues
os.environ["ENABLE_LOGGING_MIDDLEWARE"] = "false"

# Import all models to ensure they are registered in Base.metadata before create_all()
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.imports.models import ImportHistory
from app.modules.alerts.models import Alert
from app.modules.reports.models import DailyReport

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    """Reset database before and after each test."""
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass  # Ignore errors if tables don't exist or are in inconsistent state
    Base.metadata.create_all(bind=engine)
    yield
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass  # Ignore errors if tables don't exist or are in inconsistent state


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Always rollback to avoid PendingRollbackError
        db.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database session override."""
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def seed_roles(db_session: Session) -> None:
    """Seed roles for authentication tests."""
    for role_name in ["admin", "logistica", "gestor", "auditoria"]:
        db_session.add(Role(name=role_name))
    db_session.flush()  # Use flush instead of commit since we rollback at teardown


@pytest.fixture
def seed_carrier(db_session: Session):
    """Seed a test carrier for import tests."""
    carrier = Carrier(name="Test Carrier")
    db_session.add(carrier)
    db_session.flush()
    db_session.refresh(carrier)
    return carrier


def create_user_with_roles(db: Session, email: str, password: str, roles: list[str]) -> User:
    """Create a test user with specified roles."""
    user = User(email=email, full_name=email.split("@")[0], password_hash=hash_password(password), is_active=True)
    db.add(user)
    db.flush()
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        user.roles.append(role)
    db.flush()
    db.refresh(user)
    return user


@pytest.fixture
def seed_braspress_carrier(db_session: Session):
    """Seed a fake Braspress carrier for Braspress import tests."""
    carrier = Carrier(name="Braspress")
    db_session.add(carrier)
    db_session.flush()
    db_session.refresh(carrier)
    return carrier


def login(client: TestClient, email: str, password: str) -> str:
    """Helper function to login and return access token."""
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(db_session: Session, client: TestClient, seed_roles) -> dict[str, str]:
    """Create authentication headers for a test user."""
    create_user_with_roles(db_session, "test@example.com", "test123", ["admin"])
    token = login(client, "test@example.com", "test123")
    return {"Authorization": f"Bearer {token}"}
