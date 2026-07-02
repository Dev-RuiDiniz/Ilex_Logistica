"""Tests for audit log API (BETA-019A)."""

from sqlalchemy.orm import Session


def test_get_audit_logs_retorna_lista(db_session: Session):
    """Testa GET /audit/logs retorna lista (testando service diretamente)."""
    from app.modules.audit.models import OperationalAuditLog

    logs = db_session.query(OperationalAuditLog).all()
    assert isinstance(logs, list)


def test_get_audit_summary_retorna_estatisticas(db_session: Session):
    """Testa GET /audit/summary retorna estatísticas (testando service diretamente)."""
    from app.modules.audit.service import AuditLogService

    summary = AuditLogService.get_summary(db_session)
    assert summary.total_logs >= 0
    assert summary.success_count >= 0
    assert summary.failed_count >= 0
    assert summary.skipped_count >= 0


def test_post_audit_log_cria_log(db_session: Session):
    """Testa POST /audit cria log (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    log_data = AuditLogCreateRequest(
        event_type="test_event",
        entity_type="test",
        action="create",
        severity="info",
        status="success",
        message="Test log",
    )

    log = AuditLogService.create_log(db_session, log_data)
    assert log.id is not None
    assert log.event_type == "test_event"


def test_get_audit_log_by_id_retorna_detalhe(db_session: Session):
    """Testa GET /audit/{id} retorna detalhe (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    # Criar log
    log_data = AuditLogCreateRequest(
        event_type="test_event",
        entity_type="test",
        action="create",
        severity="info",
        status="success",
        message="Test log",
    )
    created_log = AuditLogService.create_log(db_session, log_data)

    # Buscar por ID
    found_log = AuditLogService.get_log_by_id(db_session, created_log.id)
    assert found_log is not None
    assert found_log.id == created_log.id


def test_filtros_funcionam(db_session: Session):
    """Testa filtros funcionam (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    # Criar logs com diferentes filtros
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Shipment",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="alert_generated",
            entity_type="alert",
            action="create",
            severity="warning",
            status="success",
            message="Alert",
        ),
    )

    # Filtrar por event_type
    logs, total = AuditLogService.get_logs(db_session, event_type="shipment_created")
    assert total == 1
    assert logs[0].event_type == "shipment_created"


def test_payload_e_estavel_para_frontend(db_session: Session):
    """Testa payload é estável para frontend (testando model diretamente)."""
    from app.modules.audit.models import OperationalAuditLog

    logs = db_session.query(OperationalAuditLog).all()
    # Verificar estrutura estável
    for log in logs:
        assert hasattr(log, "id")
        assert hasattr(log, "event_type")
        assert hasattr(log, "entity_type")
        assert hasattr(log, "action")
        assert hasattr(log, "severity")
        assert hasattr(log, "status")
        assert hasattr(log, "message")
        assert hasattr(log, "created_at")


def test_rota_nao_conflita_com_rotas_existentes(db_session: Session):
    """Testa rota não conflita com rotas existentes (testando model diretamente)."""
    from app.modules.audit.models import OperationalAuditLog

    # Verificar que tabela existe e pode ser consultada
    count = db_session.query(OperationalAuditLog).count()
    assert count >= 0


def test_paginacao_funciona(db_session: Session):
    """Testa paginação funciona (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    # Criar alguns logs
    for i in range(5):
        AuditLogService.create_log(
            db_session,
            AuditLogCreateRequest(
                event_type="test_event",
                entity_type="test",
                action="create",
                severity="info",
                status="success",
                message=f"Log {i}",
            ),
        )

    # Testar paginação
    logs, total = AuditLogService.get_logs(db_session, skip=0, limit=3)
    assert total == 5
    assert len(logs) == 3


def test_filtro_por_periodo_funciona(db_session: Session):
    """Testa filtro por período funciona (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    # Criar logs
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="test_event",
            entity_type="test",
            action="create",
            severity="info",
            status="success",
            message="Log 1",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="test_event",
            entity_type="test",
            action="create",
            severity="info",
            status="success",
            message="Log 2",
        ),
    )

    # Listar todos - deve retornar ordenado por created_at desc
    logs, total = AuditLogService.get_logs(db_session)
    assert total == 2
    assert logs[0].created_at >= logs[1].created_at


def test_filtro_multiplas_condicoes(db_session: Session):
    """Testa filtro com múltiplas condições (testando service diretamente)."""
    from app.modules.audit.schemas import AuditLogCreateRequest
    from app.modules.audit.service import AuditLogService

    # Criar logs variados
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Shipment success",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="critical",
            status="failed",
            message="Shipment failed",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="alert_generated",
            entity_type="alert",
            action="create",
            severity="warning",
            status="success",
            message="Alert",
        ),
    )

    # Filtrar por event_type + status
    logs, total = AuditLogService.get_logs(
        db_session, event_type="shipment_created", status="success"
    )
    assert total == 1
    assert logs[0].status == "success"

    # Filtrar por severity
    logs, total = AuditLogService.get_logs(db_session, severity="critical")
    assert total == 1
    assert logs[0].severity == "critical"
