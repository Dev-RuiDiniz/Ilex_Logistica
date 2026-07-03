import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.modules.users.schemas import UserCreateRequest
from conftest import create_user_with_roles


def test_tempos_de_token_seguem_politica_operacional():
    settings = Settings()
    assert settings.jwt_access_minutes == 15
    assert settings.jwt_refresh_minutes == 60 * 24 * 7


@pytest.mark.parametrize("password", [
    "Curta1!",
    "semsimbolo123A",
    "SEMMINUSCULA123!",
    "semmaiuscula123!",
    "SemNumero!!!!",
])
def test_nova_senha_fraca_e_rejeitada(password: str):
    with pytest.raises(ValidationError):
        UserCreateRequest(email="novo@example.com", full_name="Novo", password=password)


def test_nova_senha_forte_e_aceita():
    request = UserCreateRequest(
        email="novo@example.com", full_name="Novo", password="SenhaForte123!"
    )
    assert request.password == "SenhaForte123!"


def test_refresh_rotaciona_token_e_rejeita_o_anterior(client, db_session, seed_roles):
    create_user_with_roles(db_session, "rotate@example.com", "123456", ["admin"])
    login = client.post("/api/v1/auth/login", json={"email": "rotate@example.com", "password": "123456"})
    original = login.json()["refresh_token"]

    rotated = client.post("/api/v1/auth/refresh", json={"refresh_token": original})

    assert rotated.status_code == 200
    assert rotated.json()["refresh_token"] != original
    assert client.post("/api/v1/auth/refresh", json={"refresh_token": original}).status_code == 401
