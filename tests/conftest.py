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


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
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
    db_session.flush()


def create_user_with_roles(db: Session, email: str, password: str, roles: list[str]) -> User:
    user = User(email=email, full_name=email.split("@")[0], password_hash=hash_password(password), is_active=True)
    db.add(user)
    db.flush()
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        user.roles.append(role)
    db.flush()
    db.refresh(user)
    return user
