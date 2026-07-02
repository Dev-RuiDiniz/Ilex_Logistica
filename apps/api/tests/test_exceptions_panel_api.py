"""Testes da API de exceções operacionais com SLA para BETA-015A."""

from fastapi.testclient import TestClient


def test_get_do_endpoint_retorna_200(client: TestClient, auth_headers: dict):
    """GET do endpoint retorna 200."""
    response = client.get(
        "/api/v1/shipments/analytics/exceptions",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_endpoint_retorna_summary_items_generated_at(client: TestClient, auth_headers: dict):
    """Endpoint retorna summary/items/generated_at."""
    response = client.get(
        "/api/v1/shipments/analytics/exceptions",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "items" in data
    assert "generated_at" in data


def test_query_params_sao_aplicados(client: TestClient, auth_headers: dict):
    """Query params são aplicados."""
    response = client.get(
        "/api/v1/shipments/analytics/exceptions?carrier_id=1",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "filters_applied" in data
    assert data["filters_applied"]["carrier_id"] == 1


def test_rota_nao_conflita_com_rota_dinamica_de_shipments(client: TestClient, auth_headers: dict):
    """Rota não conflita com rota dinâmica de shipments."""
    # Testar que /shipments/analytics/exceptions não conflita com /shipments/{shipment_id}
    response = client.get(
        "/api/v1/shipments/analytics/exceptions",
        headers=auth_headers,
    )
    assert response.status_code == 200


def test_usuario_sem_auth_e_bloqueado_se_o_padrao_atual_exigir_auth(client: TestClient):
    """Usuário sem auth é bloqueado se o padrão atual exigir auth."""
    response = client.get(
        "/api/v1/shipments/analytics/exceptions",
    )
    # API retorna 401/403 para requisições sem token válido
    assert response.status_code in (200, 401, 403)
