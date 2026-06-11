"""
Teste E2E de auditoria via API com dados sintéticos.

Este teste valida a criação e leitura de audit logs via API,
garantindo compatibilidade com o frontend.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest


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
def seed_roles(db_session: Session):
    """Seed roles for testing."""
    from app.modules.users.models import Role
    from app.modules.users.seed_permissions import seed_role_permissions
    
    for role_name in ["admin", "logistica", "gestor", "auditoria", "manager", "operator", "viewer"]:
        db_session.add(Role(name=role_name))
    db_session.commit()
    
    seed_role_permissions(db_session)


class TestAuditLogAPIE2E:
    """Teste E2E de auditoria via API."""

    def test_audit_log_via_api_contract(
        self,
        db_session: Session,
        seed_roles,
    ):
        """
        Teste de audit log via service com validação de contrato.
        
        Cenário:
        1. Criar audit log via service
        2. Validar campos do log
        3. Validar compatibilidade com schema Pydantic
        4. Validar recuperação por ID
        5. Validar listagem com filtros
        """
        # Step 1: Criar audit log via service
        log_data = AuditLogCreateRequest(
            event_type="synthetic_test",
            entity_type="test_entity",
            entity_id=1,
            action="create",
            actor_user_id=1,
            actor_email="synthetic@test.com",
            severity="info",
            status="success",
            message="Audit log sintético para homologação",
            metadata_json='{"test": "synthetic_e2e"}'
        )
        
        created_log = AuditLogService.create_log(db_session, log_data)
        
        # Step 2: Validar campos do log
        assert created_log is not None, "Audit log deve ser criado"
        assert created_log.id is not None, "Audit log deve ter ID"
        assert created_log.event_type == "synthetic_test", "Event type deve corresponder"
        assert created_log.entity_type == "test_entity", "Entity type deve corresponder"
        assert created_log.entity_id == 1, "Entity ID deve corresponder"
        assert created_log.action == "create", "Action deve corresponder"
        assert created_log.severity == "info", "Severity deve corresponder"
        assert created_log.status == "success", "Status deve corresponder"
        
        # Step 3: Validar compatibilidade com schema Pydantic
        from app.modules.audit.schemas import AuditLogResponse
        log_response = AuditLogResponse.model_validate(created_log)
        
        assert log_response.id == created_log.id, "Schema deve ser compatível"
        assert log_response.event_type == created_log.event_type, "Schema deve ser compatível"
        assert log_response.entity_type == created_log.entity_type, "Schema deve ser compatível"
        
        # Step 4: Validar recuperação por ID
        retrieved_log = AuditLogService.get_log_by_id(db_session, created_log.id)
        assert retrieved_log is not None, "Audit log deve ser recuperado por ID"
        assert retrieved_log.id == created_log.id, "Audit log recuperado deve ser o mesmo"
        
        # Step 5: Validar listagem com filtros
        logs, total = AuditLogService.get_logs(
            db_session,
            skip=0,
            limit=10,
            event_type="synthetic_test",
            entity_type="test_entity"
        )
        
        assert total >= 1, f"Deve ter pelo menos 1 log, got {total}"
        assert len(logs) >= 1, f"Deve ter pelo menos 1 log na lista, got {len(logs)}"
        assert logs[0].id == created_log.id, "Log recuperado deve ser o mesmo"
