import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.modules.users.schemas import UserCreateRequest


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
