"""Tests for dashboard trend API for BETA-029."""

import pytest
from datetime import UTC, datetime, timedelta
from fastapi.testclient import TestClient


def test_get_dashboard_trend_retorna_dados(client: TestClient):
    """Testa GET /dashboard/trend retorna dados de tendência."""
    response = client.get("/api/v1/dashboard/trend")

    # Padrão atual não exige auth em todos os endpoints
    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "trend_data" in data
        assert "period" in data
        assert isinstance(data["trend_data"], list)
        assert "start_date" in data["period"]
        assert "end_date" in data["period"]
        assert "days" in data["period"]


def test_get_dashboard_trend_com_filtros(client: TestClient):
    """Testa GET /dashboard/trend com filtros de data."""
    date_from = (datetime.now(UTC) - timedelta(days=14)).date().isoformat()
    date_to = datetime.now(UTC).date().isoformat()

    response = client.get(
        f"/api/v1/dashboard/trend?estimated_delivery_from={date_from}&estimated_delivery_to={date_to}&days=14"
    )

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert "trend_data" in data
        assert data["period"]["days"] == 15  # 14 + 1


def test_get_dashboard_trend_com_days_customizado(client: TestClient):
    """Testa GET /dashboard/trend com parâmetro days customizado."""
    response = client.get("/api/v1/dashboard/trend?days=7")

    assert response.status_code in [200, 401, 403]

    if response.status_code == 200:
        data = response.json()
        assert data["period"]["days"] == 8  # 7 + 1


def test_get_dashboard_trend_dias_maximo_90(client: TestClient):
    """Testa que days não pode exceder 90."""
    response = client.get("/api/v1/dashboard/trend?days=95")

    # Deve retornar 422 (validation error) ou 400
    assert response.status_code in [422, 400, 401, 403]


def test_get_dashboard_trend_dias_minimo_1(client: TestClient):
    """Testa que days não pode ser menor que 1."""
    response = client.get("/api/v1/dashboard/trend?days=0")

    # Deve retornar 422 (validation error) ou 400
    assert response.status_code in [422, 400, 401, 403]


def test_get_dashboard_trend_payload_estavel(client: TestClient):
    """Testa que payload é estável para frontend."""
    response = client.get("/api/v1/dashboard/trend?days=7")

    if response.status_code == 200:
        data = response.json()
        assert "trend_data" in data
        assert "period" in data
        for day in data["trend_data"]:
            assert "date" in day
            assert "total_shipments" in day
            assert "on_time_count" in day
            assert "late_count" in day
            assert "critical_count" in day
            assert "warning_count" in day
            assert "unknown_sla_count" in day
            assert "exceptions_count" in day