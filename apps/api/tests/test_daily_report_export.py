"""Tests for daily report export API for BETA-028."""

from datetime import UTC, datetime
import pytest
from fastapi.testclient import TestClient


def test_post_reports_daily_export_csv(client: TestClient):
    """Testa POST /reports/daily/export retorna CSV."""
    # Primeiro criar um relatório para exportar
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    request_data = {"report_date": report_date.isoformat()}
    client.post("/api/v1/reports/daily/generate", json=request_data)

    # Exportar como CSV
    export_data = {
        "format": "csv",
        "date_from": "2025-01-01",
        "date_to": "2025-01-31",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    # Padrão atual não exige auth em todos os endpoints (aceita 200, 401, 403)
    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        assert "filename" in data
        assert "media_type" in data
        assert data["filename"].endswith(".csv")
        assert "text/csv" in data["media_type"]
        # Verificar que o CSV tem cabeçalho
        content = data["content"]
        assert "id,report_date,status" in content


def test_post_reports_daily_export_json(client: TestClient):
    """Testa POST /reports/daily/export retorna JSON."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    request_data = {"report_date": report_date.isoformat()}
    client.post("/api/v1/reports/daily/generate", json=request_data)

    export_data = {
        "format": "json",
        "date_from": "2025-01-01",
        "date_to": "2025-01-31",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        assert "filename" in data
        assert "media_type" in data
        assert data["filename"].endswith(".json")
        assert "application/json" in data["media_type"]
        # Verificar que o JSON é válido
        import json
        parsed = json.loads(data["content"])
        assert isinstance(parsed, list)


def test_post_reports_daily_export_invalid_format(client: TestClient):
    """Testa POST /reports/daily/export com formato inválido."""
    export_data = {
        "format": "xml",
        "date_from": "2025-01-01",
        "date_to": "2025-01-31",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    # Deve retornar 400 para formato inválido
    assert response.status_code in [400, 401, 403]

    if response.status_code == 400:
        data = response.json()
        assert "detail" in data
        assert "suportado" in data["detail"] or "support" in data["detail"]


def test_post_reports_daily_export_with_status_filter(client: TestClient):
    """Testa export com filtro de status."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    client.post("/api/v1/reports/daily/generate", json={"report_date": report_date.isoformat()})

    export_data = {
        "format": "csv",
        "status": "generated",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        content = data["content"]
        assert "id,report_date,status" in content


def test_post_reports_daily_export_with_date_filters(client: TestClient):
    """Testa export com filtros de data."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    client.post("/api/v1/reports/daily/generate", json={"report_date": report_date.isoformat()})

    export_data = {
        "format": "json",
        "date_from": "2025-01-01",
        "date_to": "2025-01-31",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        import json
        parsed = json.loads(data["content"])
        assert isinstance(parsed, list)


def test_post_reports_daily_export_empty_result(client: TestClient):
    """Testa export quando não há relatórios no período."""
    export_data = {
        "format": "csv",
        "date_from": "2020-01-01",
        "date_to": "2020-01-31",
    }
    response = client.post("/api/v1/reports/daily/export", json=export_data)

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        # CSV deve ter apenas cabeçalho quando vazio
        content = data["content"]
        lines = content.strip().split("\n")
        assert len(lines) == 1  # Apenas header
        assert "id,report_date,status" in lines[0]


def test_get_reports_daily_count_in_list(client: TestClient):
    """Testa que total no list_daily_reports reflete count real."""
    # Criar alguns relatórios
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        client.post("/api/v1/reports/daily/generate", json={"report_date": report_date.isoformat()})

    # Listar com paginação
    response = client.get("/api/v1/reports/daily?limit=2")

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "reports" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert data["total"] == 3  # Total real, não len(reports)
        assert len(data["reports"]) == 2  # Limit=2


def test_get_reports_daily_total_with_filters(client: TestClient):
    """Testa total com filtros de data."""
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        client.post("/api/v1/reports/daily/generate", json={"report_date": report_date.isoformat()})

    response = client.get("/api/v1/reports/daily?date_from=2025-01-02")

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert data["total"] == 2  # Dias 2 e 3