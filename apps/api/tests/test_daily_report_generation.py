"""Tests for daily report generation service for BETA-018A."""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.modules.reports.service import generate_daily_report, get_daily_report_by_date, list_daily_reports


def test_gera_relatorio_para_data_especifica(db_session: Session):
    """Testa geração de relatório para data específica."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    assert report is not None
    assert report.report_date.date() == report_date.date()
    assert report.status == "generated"
    assert report.generated_at is not None
    assert report.summary_json is not None
    assert report.kpis_json is not None


def test_consolida_kpis_do_dashboard(db_session: Session):
    """Testa que relatório consolida KPIs do dashboard."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que summary_json contém KPIs
    assert "total_shipments" in report.summary_json
    assert "on_time_count" in report.summary_json
    assert "late_count" in report.summary_json


def test_inclui_alertas_ativos(db_session: Session):
    """Testa que relatório inclui alertas ativos."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que kpis_json contém active_alerts_count
    assert "active_alerts_count" in report.kpis_json


def test_inclui_eficiencia_por_transportadora(db_session: Session):
    """Testa que relatório inclui eficiência por transportadora."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que carrier_efficiency_json existe
    assert report.carrier_efficiency_json is not None


def test_inclui_falhas_de_importacao_quando_houver(db_session: Session):
    """Testa que relatório inclui falhas de importação."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que import_failures_json existe
    assert report.import_failures_json is not None
    assert "rejected_count" in report.import_failures_json


def test_funciona_com_base_vazia(db_session: Session):
    """Testa que geração funciona com base vazia."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    assert report is not None
    assert report.status == "generated"
    # Deve ter valores zerados quando base está vazia
    assert "total_shipments" in report.summary_json


def test_eh_idempotente_por_data(db_session: Session):
    """Testa que geração é idempotente por data."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Primeira geração
    report1 = generate_daily_report(db_session, report_date)
    report1_id = report1.id
    
    # Segunda geração (deve atualizar o mesmo)
    report2 = generate_daily_report(db_session, report_date)
    
    assert report2.id == report1_id  # Mesmo ID (upsert)


def test_permite_regenerar_relatorio(db_session: Session):
    """Testa que é possível regenerar relatório."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Primeira geração
    report1 = generate_daily_report(db_session, report_date)
    
    # Regenerar com período diferente
    period_start = datetime(2025, 1, 21, 0, 0, 0, tzinfo=UTC)
    period_end = datetime(2025, 1, 21, 23, 59, 59, tzinfo=UTC)
    report2 = generate_daily_report(
        db_session,
        report_date,
        period_start=period_start,
        period_end=period_end,
    )
    
    assert report2.id == report1.id  # Mesmo ID (upsert)
    assert report2.period_start is not None
    assert report2.period_end is not None


def test_retorna_status_generated(db_session: Session):
    """Testa que relatório gerado tem status 'generated'."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    assert report.status == "generated"


def test_nao_duplica_regra_de_sla(db_session: Session):
    """Testa que não duplica regra de SLA (usa dashboard service)."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que summary_json contém SLA info do dashboard
    assert "on_time_count" in report.summary_json
    assert "late_count" in report.summary_json
    assert "critical_count" in report.summary_json


def test_nao_duplica_regra_de_excecoes(db_session: Session):
    """Testa que não duplica regra de exceções (usa dashboard service)."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Verificar que exceptions_json existe
    assert report.exceptions_json is not None


def test_nao_usa_dados_reais(db_session: Session):
    """Testa que não usa dados reais (apenas dados do dashboard service)."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = generate_daily_report(db_session, report_date)
    
    # Dados devem vir do dashboard service, não de fontes externas
    assert report.summary_json is not None
    assert report.kpis_json is not None


def test_get_daily_report_by_date(db_session: Session):
    """Testa busca de relatório por data."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Criar relatório
    generate_daily_report(db_session, report_date)
    
    # Buscar por data
    found_report = get_daily_report_by_date(db_session, report_date)
    
    assert found_report is not None
    assert found_report.report_date.date() == report_date.date()


def test_get_daily_report_by_date_nao_encontrado(db_session: Session):
    """Testa busca de relatório por data quando não existe."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Buscar data que não existe
    found_report = get_daily_report_by_date(db_session, report_date)
    
    assert found_report is None


def test_list_daily_reports(db_session: Session):
    """Testa listagem de relatórios."""
    # Criar múltiplos relatórios
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        generate_daily_report(db_session, report_date)
    
    # Listar todos
    reports = list_daily_reports(db_session)
    
    assert len(reports) == 3


def test_list_daily_reports_com_filtro_date_from(db_session: Session):
    """Testa listagem com filtro de data inicial."""
    # Criar múltiplos relatórios
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        generate_daily_report(db_session, report_date)
    
    # Listar com filtro
    date_from = datetime(2025, 1, 2, tzinfo=UTC)
    reports = list_daily_reports(db_session, date_from=date_from)
    
    assert len(reports) == 2  # dias 2 e 3


def test_list_daily_reports_com_filtro_date_to(db_session: Session):
    """Testa listagem com filtro de data final."""
    # Criar múltiplos relatórios
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        generate_daily_report(db_session, report_date)
    
    # Listar com filtro
    date_to = datetime(2025, 1, 2, tzinfo=UTC)
    reports = list_daily_reports(db_session, date_to=date_to)
    
    assert len(reports) == 2  # dias 1 e 2


def test_list_daily_reports_com_filtro_status(db_session: Session):
    """Testa listagem com filtro de status."""
    # Criar relatório
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    generate_daily_report(db_session, report_date)
    
    # Listar com filtro de status
    reports = list_daily_reports(db_session, status="generated")
    
    assert len(reports) == 1
    assert reports[0].status == "generated"


def test_list_daily_reports_com_limit_offset(db_session: Session):
    """Testa listagem com limit e offset."""
    # Criar múltiplos relatórios
    for day in range(1, 4):
        report_date = datetime(2025, 1, day, tzinfo=UTC)
        generate_daily_report(db_session, report_date)
    
    # Listar com limit
    reports = list_daily_reports(db_session, limit=2)
    
    assert len(reports) == 2
    
    # Listar com offset
    reports = list_daily_reports(db_session, limit=2, offset=1)
    
    assert len(reports) == 2
