"""
Teste de contrato frontend/backend para dados sintéticos.

Este teste valida que os schemas Pydantic do backend são compatíveis
com os tipos TypeScript do frontend para as páginas críticas.
"""

import pytest
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.reports.service import generate_daily_report
from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest
from app.modules.reports.schemas import DailyReportResponse
from app.modules.shipments.models import Shipment
from app.modules.carriers.models import Carrier


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
    """Seed a test carrier for contract tests."""
    carrier = Carrier(name="Braspress")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    return carrier


class TestFrontendBackendContract:
    """Teste de contrato frontend/backend para dados sintéticos."""

    def test_daily_report_contract_compatibility(
        self,
        db_session: Session,
        seed_braspress_carrier,
    ):
        """
        Teste de contrato: valida que dados sintéticos do backend são compatíveis com frontend.
        
        Cenário:
        1. Criar shipments sintéticos
        2. Gerar relatório diário
        3. Validar que schema Pydantic é compatível com TypeScript
        4. Validar que campos JSON são serializáveis
        """
        # Step 1: Criar shipments sintéticos
        today = date.today()
        shipment = Shipment(
            tracking_code="SYNTH-CONTRACT-001",
            carrier_id=seed_braspress_carrier.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=5),
            actual_delivery=today - timedelta(days=4),
            recipient_name="Cliente Contrato 1",
            recipient_phone="11999999999",
            origin_address="Rua Origem 1, SP",
            destination_address="Rua Destino 1, SP",
            invoice_number="INV-CON-001",
            invoice_value=1000.00,
            freight_value=50.00,
            customer_name="Cliente Contrato 1",
            destination_uf="SP"
        )
        db_session.add(shipment)
        db_session.commit()
        
        # Step 2: Gerar relatório diário
        report = generate_daily_report(db_session, datetime.combine(today, datetime.min.time()))
        
        # Step 3: Validar que schema Pydantic é compatível com TypeScript
        report_response = DailyReportResponse.model_validate(report)
        
        # Validar que todos os campos são serializáveis (JSON compatível)
        report_dict = report_response.model_dump()
        
        # Validar que campos JSON são strings válidas
        if report.summary_json:
            import json
            try:
                json.loads(report.summary_json)
            except:
                pytest.fail("summary_json deve ser JSON válido")
        
        if report.kpis_json:
            import json
            try:
                json.loads(report.kpis_json)
            except:
                pytest.fail("kpis_json deve ser JSON válido")
        
        if report.exceptions_json:
            import json
            try:
                json.loads(report.exceptions_json)
            except:
                pytest.fail("exceptions_json deve ser JSON válido")
        
        if report.alerts_json:
            import json
            try:
                json.loads(report.alerts_json)
            except:
                pytest.fail("alerts_json deve ser JSON válido")
        
        if report.carrier_efficiency_json:
            import json
            try:
                json.loads(report.carrier_efficiency_json)
            except:
                pytest.fail("carrier_efficiency_json deve ser JSON válido")
        
        # Step 4: Validar que campos críticos do frontend estão presentes
        # Campos esperados pelo frontend (baseado em daily-report-api.test.tsx)
        assert report_dict["id"] is not None, "Campo 'id' deve estar presente"
        assert report_dict["report_date"] is not None, "Campo 'report_date' deve estar presente"
        assert report_dict["status"] is not None, "Campo 'status' deve estar presente"
        assert report_dict["summary_json"] is not None, "Campo 'summary_json' deve estar presente"
    
    def test_audit_log_contract_compatibility(
        self,
        db_session: Session,
    ):
        """
        Teste de contrato: valida que audit logs são compatíveis com frontend.
        
        Cenário:
        1. Criar audit log sintético
        2. Validar que schema Pydantic é compatível com TypeScript
        3. Validar que campos JSON são serializáveis
        """
        # Step 1: Criar audit log sintético
        log_data = AuditLogCreateRequest(
            event_type="synthetic_contract_test",
            entity_type="test_entity",
            entity_id=1,
            action="create",
            actor_user_id=1,
            actor_email="synthetic@test.com",
            severity="info",
            status="success",
            message="Audit log sintético para teste de contrato",
            metadata_json='{"test": "synthetic_e2e"}'
        )
        
        created_log = AuditLogService.create_log(db_session, log_data)
        
        # Step 2: Validar que schema Pydantic é compatível com TypeScript
        from app.modules.audit.schemas import AuditLogResponse
        log_response = AuditLogResponse.model_validate(created_log)
        
        # Step 3: Validar que todos os campos são serializáveis (JSON compatível)
        log_dict = log_response.model_dump()
        
        # Validar que campos JSON são strings válidas
        if log_dict.get("metadata_json"):
            import json
            try:
                json.loads(log_dict["metadata_json"])
            except:
                pytest.fail("metadata_json deve ser JSON válido")
        
        if log_dict.get("before_json"):
            import json
            try:
                json.loads(log_dict["before_json"])
            except:
                pytest.fail("before_json deve ser JSON válido")
        
        if log_dict.get("after_json"):
            import json
            try:
                json.loads(log_dict["after_json"])
            except:
                pytest.fail("after_json deve ser JSON válido")
        
        # Step 4: Validar que campos críticos do frontend estão presentes
        # Campos esperados pelo frontend (baseado em audit-api.test.tsx)
        assert log_dict["id"] is not None, "Campo 'id' deve estar presente"
        assert log_dict["event_type"] is not None, "Campo 'event_type' deve estar presente"
        assert log_dict["entity_type"] is not None, "Campo 'entity_type' deve estar presente"
        assert log_dict["action"] is not None, "Campo 'action' deve estar presente"
        assert log_dict["severity"] is not None, "Campo 'severity' deve estar presente"
        assert log_dict["status"] is not None, "Campo 'status' deve estar presente"
        assert log_dict["created_at"] is not None, "Campo 'created_at' deve estar presente"
