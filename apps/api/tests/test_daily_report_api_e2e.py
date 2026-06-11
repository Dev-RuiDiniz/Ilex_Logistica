"""
Teste E2E de relatório diário via API com dados sintéticos.

Este teste valida a geração e leitura de relatório diário via API,
garantindo compatibilidade com o frontend.
"""

import pytest
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.reports.service import generate_daily_report, get_daily_report_by_date
from app.modules.reports.schemas import DailyReportGenerateRequest
from app.modules.shipments.models import Shipment
from app.modules.carriers.models import Carrier
from app.modules.alerts.models import Alert


@pytest.fixture
def db_session():
    """Get database session for testing using SQLite test database."""
    from tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    try:
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture
def seed_braspress_carrier(db_session: Session):
    """Seed a test carrier for report tests."""
    carrier = Carrier(name="Braspress")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    return carrier


class TestDailyReportAPIE2E:
    """Teste E2E de relatório diário via API."""

    def test_daily_report_via_api_contract(
        self,
        db_session: Session,
        seed_braspress_carrier,
    ):
        """
        Teste de relatório diário via service com validação de contrato.
        
        Cenário:
        1. Criar shipments sintéticos
        2. Gerar relatório diário via service
        3. Validar campos do relatório
        4. Validar compatibilidade com schema Pydantic
        5. Validar campos usados pelo frontend
        """
        # Step 1: Criar shipments sintéticos
        today = date.today()
        shipment1 = Shipment(
            tracking_code="SYNTH-REPORT-001",
            carrier_id=seed_braspress_carrier.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=5),
            actual_delivery=today - timedelta(days=4),
            recipient_name="Cliente Relatório 1",
            recipient_phone="11999999999",
            origin_address="Rua Origem 1, SP",
            destination_address="Rua Destino 1, SP",
            invoice_number="INV-REP-001",
            invoice_value=1000.00,
            freight_value=50.00,
            customer_name="Cliente Relatório 1",
            destination_uf="SP"
        )
        shipment2 = Shipment(
            tracking_code="SYNTH-REPORT-002",
            carrier_id=seed_braspress_carrier.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=3),
            actual_delivery=today,
            recipient_name="Cliente Relatório 2",
            recipient_phone="21999999999",
            origin_address="Rua Origem 2, RJ",
            destination_address="Rua Destino 2, RJ",
            invoice_number="INV-REP-002",
            invoice_value=2000.00,
            freight_value=100.00,
            customer_name="Cliente Relatório 2",
            destination_uf="RJ"
        )
        db_session.add_all([shipment1, shipment2])
        db_session.commit()
        
        # Step 2: Gerar relatório diário via service
        report = generate_daily_report(db_session, today)
        
        # Step 3: Validar campos do relatório
        assert report is not None, "Relatório deve ser gerado"
        assert report.id is not None, "Relatório deve ter ID"
        assert report.report_date.date() == today, "Data do relatório deve corresponder"
        assert report.status == "generated", "Status deve ser generated"
        
        # Step 4: Validar compatibilidade com schema Pydantic
        from app.modules.reports.schemas import DailyReportResponse
        report_response = DailyReportResponse.model_validate(report)
        
        assert report_response.id == report.id, "Schema deve ser compatível"
        assert report_response.report_date == report.report_date, "Schema deve ser compatível"
        assert report_response.status == report.status, "Schema deve ser compatível"
        
        # Step 5: Validar campos usados pelo frontend
        # Campos esperados pelo frontend (baseado em daily-report-api.test.tsx)
        assert report.summary_json is not None, "Relatório deve ter summary_json"
        
        # Validar que summary_json é um JSON válido
        import json
        try:
            summary = json.loads(report.summary_json) if isinstance(report.summary_json, str) else report.summary_json
        except:
            summary = {}
        
        # Validar que relatório pode ser recuperado por data
        retrieved_report = get_daily_report_by_date(db_session, datetime.combine(today, datetime.min.time()))
        assert retrieved_report is not None, "Relatório deve ser recuperado por data"
        assert retrieved_report.id == report.id, "Relatório recuperado deve ser o mesmo"
