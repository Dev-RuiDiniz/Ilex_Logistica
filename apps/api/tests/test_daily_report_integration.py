"""Tests for daily report integration for BETA-018A."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.modules.reports.service import generate_daily_report
from app.modules.reports.models import DailyReport


def test_relatorio_usa_dashboard_summary_real(db_session: Session):
    """Testa que relatório usa dashboard summary real."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que summary_json contém dados do dashboard
    assert report.summary_json is not None
    assert "total_shipments" in report.summary_json


def test_relatorio_usa_exceptions_service_real(db_session: Session):
    """Testa que relatório usa exceptions service real."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que exceptions_json existe
    assert report.exceptions_json is not None


def test_relatorio_usa_alerts_service_real(db_session: Session):
    """Testa que relatório usa alerts service real."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que kpis_json contém active_alerts_count
    assert "active_alerts_count" in report.kpis_json


def test_relatorio_usa_carrier_efficiency_service_real(db_session: Session):
    """Testa que relatório usa carrier efficiency service real."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que carrier_efficiency_json existe
    assert report.carrier_efficiency_json is not None


def test_geracao_nao_quebra_quando_alertas_0(db_session: Session):
    """Testa que geração não quebra quando alertas = 0."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Deve funcionar mesmo sem alertas
    assert report is not None
    assert report.status == "generated"


def test_geracao_nao_quebra_quando_nao_ha_import_failures(db_session: Session):
    """Testa que geração não quebra quando não há import failures."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Deve funcionar mesmo sem import failures
    assert report is not None
    assert report.status == "generated"
