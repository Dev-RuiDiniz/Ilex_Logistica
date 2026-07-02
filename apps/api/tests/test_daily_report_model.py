"""Tests for DailyReport model for BETA-018A."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.modules.reports.models import DailyReport


def test_cria_relatorio_diario_valido(db_session: Session):
    """Testa criação de relatório diário válido."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = DailyReport(
        report_date=report_date,
    )
    
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    
    assert report.id is not None
    assert report.report_date.date() == report_date.date()
    assert report.status == "generated"
    assert report.generated_at is not None


def test_exige_report_date(db_session: Session):
    """Testa que report_date é obrigatório."""
    report = DailyReport(
        status="generated",
    )
    
    db_session.add(report)
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.commit()


def test_valida_status(db_session: Session):
    """Testa validação de status."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Status válido
    report = DailyReport(
        report_date=report_date,
        status="generated",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    assert report.status == "generated"
    
    # Status válido alternativo
    report2 = DailyReport(
        report_date=datetime(2025, 1, 22, tzinfo=UTC),
        status="failed",
    )
    db_session.add(report2)
    db_session.commit()
    db_session.refresh(report2)
    assert report2.status == "failed"


def test_armazena_summary_kpis_exceptions_alerts_carrier_efficiency(db_session: Session):
    """Testa armazenamento de JSONs."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = DailyReport(
        report_date=report_date,
        status="generated",
        summary_json='{"total_shipments": 100, "delivered": 80}',
        kpis_json='{"on_time_count": 80, "late_count": 15}',
        exceptions_json='[{"shipment_id": 1, "priority": 1}]',
        alerts_json='[{"id": 1, "severity": "critical"}]',
        carrier_efficiency_json='[{"carrier_id": 1, "efficiency": 90.5}]',
        import_failures_json='{"rejected_count": 5}',
    )
    
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    
    assert report.summary_json == '{"total_shipments": 100, "delivered": 80}'
    assert report.kpis_json == '{"on_time_count": 80, "late_count": 15}'
    assert report.exceptions_json == '[{"shipment_id": 1, "priority": 1}]'
    assert report.alerts_json == '[{"id": 1, "severity": "critical"}]'
    assert report.carrier_efficiency_json == '[{"carrier_id": 1, "efficiency": 90.5}]'
    assert report.import_failures_json == '{"rejected_count": 5}'


def test_evita_duplicidade_por_report_date(db_session: Session):
    """Testa que report_date é único."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report1 = DailyReport(
        report_date=report_date,
        status="generated",
    )
    db_session.add(report1)
    db_session.commit()
    
    # Tentar criar segundo relatório com mesma data deve falhar
    report2 = DailyReport(
        report_date=report_date,
        status="generated",
    )
    db_session.add(report2)
    
    with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
        db_session.commit()
    
    # Rollback to clean up
    db_session.rollback()


def test_permite_regeneracao_upsert(db_session: Session):
    """Testa que regeneração é possível via upsert (delete + insert)."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Criar relatório inicial
    report1 = DailyReport(
        report_date=report_date,
        status="generated",
        summary_json='{"total_shipments": 100}',
    )
    db_session.add(report1)
    db_session.commit()
    db_session.refresh(report1)
    
    # Simular regeneração: deletar e recriar
    db_session.delete(report1)
    db_session.commit()
    
    report2 = DailyReport(
        report_date=report_date,
        status="generated",
        summary_json='{"total_shipments": 150}',  # Dados atualizados
    )
    db_session.add(report2)
    db_session.commit()
    db_session.refresh(report2)
    
    # Verificar que dados foram atualizados
    assert report2.summary_json == '{"total_shipments": 150}'


def test_status_default_generated(db_session: Session):
    """Testa que status default é 'generated'."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = DailyReport(
        report_date=report_date,
    )
    
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    
    assert report.status == "generated"


def test_generated_by_user_id_opcional(db_session: Session):
    """Testa que generated_by_user_id é opcional."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Sem user_id
    report1 = DailyReport(
        report_date=report_date,
        status="generated",
    )
    db_session.add(report1)
    db_session.commit()
    db_session.refresh(report1)
    assert report1.generated_by_user_id is None
    
    # Com user_id
    report2 = DailyReport(
        report_date=datetime(2025, 1, 22, tzinfo=UTC),
        status="generated",
        generated_by_user_id=1,
    )
    db_session.add(report2)
    db_session.commit()
    db_session.refresh(report2)
    assert report2.generated_by_user_id == 1


def test_notes_opcional(db_session: Session):
    """Testa que notes é opcional."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    # Sem notes
    report1 = DailyReport(
        report_date=report_date,
        status="generated",
    )
    db_session.add(report1)
    db_session.commit()
    db_session.refresh(report1)
    assert report1.notes is None
    
    # Com notes
    report2 = DailyReport(
        report_date=datetime(2025, 1, 22, tzinfo=UTC),
        status="generated",
        notes="Relatório gerado manualmente",
    )
    db_session.add(report2)
    db_session.commit()
    db_session.refresh(report2)
    assert report2.notes == "Relatório gerado manualmente"


def test_created_at_updated_at_preenchidos(db_session: Session):
    """Testa que created_at e updated_at são preenchidos automaticamente."""
    report_date = datetime(2025, 1, 21, tzinfo=UTC)
    
    report = DailyReport(
        report_date=report_date,
        status="generated",
    )
    
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)
    
    assert report.created_at is not None
    assert report.updated_at is not None
    assert report.generated_at is not None
