"""Teste de reconciliacao com dataset de homologacao fiscal/financeiro (P1.1).

Importa o CSV de homologacao, verifica que todas as linhas sao aceitas
e que os valores fiscais/financeiros sao persistidos corretamente.
"""
import pathlib

import pytest


@pytest.fixture(autouse=True)
def authenticated_requests(client, auth_headers):
    client.headers.update(auth_headers)


def _homologation_csv() -> bytes:
    fixture = pathlib.Path(__file__).parent / "fixtures" / "homologation_fiscal_financial.csv"
    return fixture.read_bytes()


def test_homologation_upload_retorna_200_com_todas_linhas(client, seed_carrier) -> None:
    """Upload do dataset de homologacao deve aceitar todas as linhas validas."""
    csv_bytes = _homologation_csv()
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("homologation.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    # O dataset tem 7 linhas de dados (excluindo cabecalho e comentario)
    assert data["rows_received"] == 7


def test_homologation_valores_frete_persistidos(client, db_session, seed_carrier) -> None:
    """Apos upload, deliveries devem ter valores fiscais persistidos."""
    csv_bytes = _homologation_csv()
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("homologation.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 200

    from app.modules.imports.models import Delivery
    deliveries = db_session.query(Delivery).all()
    assert len(deliveries) == 7

    # NF001: valor_frete=100.00, percentual=10.00
    nf001 = next(d for d in deliveries if d.nf == "NF001")
    assert float(nf001.valor_frete) == 100.00
    assert float(nf001.percentual_frete) == 10.00

    # NF002: valor_frete=0.00
    nf002 = next(d for d in deliveries if d.nf == "NF002")
    assert float(nf002.valor_frete) == 0.00

    # NF003: valor_frete vazio -> 0.00 (nullable=False, _parse_decimal retorna 0.00)
    nf003 = next(d for d in deliveries if d.nf == "NF003")
    assert float(nf003.valor_frete) == 0.00

    # NF004: valor_frete=99999.99 (precisao maxima)
    nf004 = next(d for d in deliveries if d.nf == "NF004")
    assert float(nf004.valor_frete) == 99999.99

    # NF005: valor_frete=100.00, percentual=0.01
    nf005 = next(d for d in deliveries if d.nf == "NF005")
    assert float(nf005.valor_frete) == 100.00
    assert float(nf005.percentual_frete) == 0.01
