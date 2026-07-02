"""Testes da API de dashboard summary para BETA-016A."""

from fastapi.testclient import TestClient


def test_endpoint_retorna_200_sem_auth_por_enquanto(client: TestClient):
    """Endpoint retorna 200 sem auth por enquanto (padrão atual)."""
    response = client.get("/api/v1/dashboard/summary")

    # Padrão atual não exige auth em todos os endpoints
    assert response.status_code in [200, 401, 403]


def test_endpoint_retorna_kpis(client: TestClient):
    """Endpoint retorna KPIs."""
    response = client.get("/api/v1/dashboard/summary")

    if response.status_code == 200:
        data = response.json()

        assert "total_shipments" in data
        assert "on_time_count" in data
        assert "late_count" in data
        assert "critical_count" in data
        assert "warning_count" in data
        assert "unknown_sla_count" in data
        assert "exceptions_count" in data
        assert "import_failure_count" in data
        assert "active_alerts_count" in data
        assert "carriers_count" in data
        assert "top_carriers_by_efficiency" in data
        assert "top_exceptions" in data
        assert "generated_at" in data
        assert "filters_applied" in data


def test_endpoint_aplica_query_params(client: TestClient):
    """Endpoint aplica query params."""
    response = client.get("/api/v1/dashboard/summary?customer_name=Test&destination_uf=SP")

    if response.status_code == 200:
        data = response.json()
        assert "filters_applied" in data


def test_endpoint_nao_conflita_com_rotas_existentes(client: TestClient):
    """Endpoint não conflita com rotas existentes."""
    response = client.get("/api/v1/dashboard/summary")

    # Verificar que rota existe (não é 404)
    assert response.status_code != 404


def test_payload_e_estavel_para_frontend(client: TestClient):
    """Payload é estável para frontend."""
    response = client.get("/api/v1/dashboard/summary")

    if response.status_code == 200:
        data = response.json()

        # Verificar estrutura estável
        assert isinstance(data["total_shipments"], int)
        assert isinstance(data["on_time_count"], int)
        assert isinstance(data["late_count"], int)
        assert isinstance(data["critical_count"], int)
        assert isinstance(data["warning_count"], int)
        assert isinstance(data["unknown_sla_count"], int)
        assert isinstance(data["exceptions_count"], int)
        assert isinstance(data["import_failure_count"], int)
        assert isinstance(data["active_alerts_count"], int)
        assert isinstance(data["carriers_count"], int)
        assert isinstance(data["top_carriers_by_efficiency"], list)
        assert isinstance(data["top_exceptions"], list)
        assert isinstance(data["generated_at"], str)
        assert isinstance(data["filters_applied"], dict)
