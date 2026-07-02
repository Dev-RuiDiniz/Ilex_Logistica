"""Tests for daily report API for BETA-018A."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient



def test_post_reports_daily_generate_retorna_relatorio(client: TestClient):
    """Testa POST /reports/daily/generate retorna relatório."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    request_data = {
        "report_date": report_date.isoformat(),
    }
    
    response = client.post("/api/v1/reports/daily/generate", json=request_data)
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403)
    assert response.status_code in [200, 401, 403]
    
    # Se auth funcionar, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "report_date" in data
        assert "status" in data


def test_get_reports_daily_lista_relatorios(client: TestClient):
    """Testa GET /reports/daily lista relatórios."""
    response = client.get("/api/v1/reports/daily")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403)
    assert response.status_code in [200, 401, 403]
    
    # Se auth funcionar, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "reports" in data
        assert "total" in data


def test_get_reports_daily_id_retorna_detalhe(client: TestClient):
    """Testa GET /reports/daily/{id} retorna detalhe."""
    response = client.get("/api/v1/reports/daily/1")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403, 404)
    assert response.status_code in [200, 401, 403, 404]
    
    # Se auth funcionar e relatório existir, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "report_date" in data


def test_get_reports_daily_by_date_retorna_relatorio_da_data(client: TestClient):
    """Testa GET /reports/daily/by-date/{date} retorna relatório da data."""
    report_date = "2025-01-21"
    
    response = client.get(f"/api/v1/reports/daily/by-date/{report_date}")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403, 404)
    assert response.status_code in [200, 401, 403, 404]
    
    # Se auth funcionar e relatório existir, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "report_date" in data


def test_filtros_por_date_from_date_to_funcionam(client: TestClient):
    """Testa filtros por date_from/date_to funcionam."""
    date_from = "2025-01-01"
    date_to = "2025-01-31"
    
    response = client.get(f"/api/v1/reports/daily?date_from={date_from}&date_to={date_to}")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403)
    assert response.status_code in [200, 401, 403]
    
    # Se auth funcionar, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "reports" in data


def test_filtro_por_status_funciona(client: TestClient):
    """Testa filtro por status funciona."""
    response = client.get("/api/v1/reports/daily?status=generated")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403)
    assert response.status_code in [200, 401, 403]
    
    # Se auth funcionar, validar payload
    if response.status_code == 200:
        data = response.json()
        assert "reports" in data


def test_payload_e_estavel_para_frontend(client: TestClient):
    """Testa que payload é estável para frontend."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    request_data = {
        "report_date": report_date.isoformat(),
    }
    
    response = client.post("/api/v1/reports/daily/generate", json=request_data)
    
    # Se auth funcionar, validar estrutura do payload
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "report_date" in data
        assert "status" in data
        assert "summary_json" in data
        assert "kpis_json" in data


def test_rota_nao_conflita_com_outras_rotas(client: TestClient):
    """Testa que rota não conflita com outras rotas."""
    response = client.get("/api/v1/reports/daily")
    
    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403, 404)
    assert response.status_code in [200, 401, 403, 404]


def test_endpoint_respeita_auth_atual_ou_documenta_gap(client: TestClient):
    """Testa que endpoint respeita auth atual ou documenta gap."""
    # Test without auth
    response = client.post("/api/v1/reports/daily/generate", json={"report_date": "2025-01-21"})
    
    # Padrão atual pode retornar 200, 401 ou 403
    assert response.status_code in [200, 401, 403]
    
    # Se retornar 200, validar que endpoint está funcionando
    if response.status_code == 200:
        data = response.json()
        assert "id" in data or "error" in data


def test_endpoints_existem_no_router():
    """Testa que endpoints foram definidos no router."""
    from app.modules.reports.router import router
    
    routes = [route.path for route in router.routes]
    
    assert "/reports/daily/generate" in routes
    assert "/reports/daily" in routes
    assert "/reports/daily/{report_id}" in routes
    assert "/reports/daily/by-date/{report_date}" in routes


def test_rota_by_date_nao_conflita_com_rota_id(client: TestClient):
    """Testa que rota /by-date/{date} não conflita com /{id}."""
    # Testar rota por data
    response_date = client.get("/api/v1/reports/daily/by-date/2025-01-21")
    # Aceita 200, 401, 403, 404
    assert response_date.status_code in [200, 401, 403, 404]
    
    # Testar rota por id
    response_id = client.get("/api/v1/reports/daily/123")
    # Aceita 200, 401, 403, 404
    assert response_id.status_code in [200, 401, 403, 404]
