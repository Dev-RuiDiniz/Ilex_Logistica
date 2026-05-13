from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from conftest import create_user_with_roles


def test_login_valido_retorna_tokens(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "123456"})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_login_invalido_retorna_401(client: TestClient, db_session: Session, seed_roles: None) -> None:
    create_user_with_roles(db_session, "admin@ilex.com", "123456", ["admin"])

    response = client.post("/api/v1/auth/login", json={"email": "admin@ilex.com", "password": "senha_errada"})

    assert response.status_code == 401


def test_token_expirado_e_recusado(client: TestClient, db_session: Session, seed_roles: None) -> None:
    user = create_user_with_roles(db_session, "audit@ilex.com", "123456", ["auditoria"])
    expired = jwt.encode(
        {
            "sub": str(user.id),
            "roles": ["auditoria"],
            "type": "access",
            "exp": int((datetime.now(UTC) - timedelta(minutes=1)).timestamp()),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get("/api/v1/carriers", headers={"Authorization": f"Bearer {expired}"})
    assert response.status_code == 401
