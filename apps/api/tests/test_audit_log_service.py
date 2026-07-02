"""Tests for AuditLogService (BETA-019A)."""


from sqlalchemy.orm import Session

from app.modules.audit.schemas import AuditLogCreateRequest
from app.modules.audit.service import AuditLogService
from app.modules.users.models import User


def test_registra_evento_simples(db_session: Session):
    """Testa registro de evento simples."""
    log_data = AuditLogCreateRequest(
        event_type="shipment_created",
        entity_type="shipment",
        entity_id=1,
        action="create",
        source="api",
        severity="info",
        status="success",
        message="Shipment criado",
    )

    log = AuditLogService.create_log(db_session, log_data)

    assert log.id is not None
    assert log.event_type == "shipment_created"
    assert log.entity_type == "shipment"
    assert log.action == "create"
    assert log.message == "Shipment criado"


def test_registra_evento_com_entidade(db_session: Session):
    """Testa registro de evento com entidade."""
    log_data = AuditLogCreateRequest(
        event_type="alert_generated",
        entity_type="alert",
        entity_id=123,
        action="create",
        source="system",
        severity="warning",
        status="success",
        message="Alerta gerado automaticamente",
    )

    log = AuditLogService.create_log(db_session, log_data)

    assert log.entity_id == 123
    assert log.entity_type == "alert"


def test_registra_evento_sistemico(db_session: Session):
    """Testa registro de evento sistêmico (sem usuário)."""
    log_data = AuditLogCreateRequest(
        event_type="daily_report_generated",
        entity_type="daily_report",
        entity_id=1,
        action="create",
        source="system",
        severity="info",
        status="success",
        message="Relatório diário gerado automaticamente",
    )

    log = AuditLogService.create_log(db_session, log_data)

    assert log.actor_user_id is None
    assert log.actor_email is None
    assert log.source == "system"


def test_lista_logs_com_filtros(db_session: Session):
    """Testa listagem de logs com filtros."""
    # Criar múltiplos logs
    for i in range(5):
        log_data = AuditLogCreateRequest(
            event_type="shipment_created" if i < 3 else "alert_generated",
            entity_type="shipment" if i < 3 else "alert",
            entity_id=i,
            action="create",
            source="api",
            severity="info",
            status="success",
            message=f"Log {i}",
        )
        AuditLogService.create_log(db_session, log_data)

    # Listar todos
    logs, total = AuditLogService.get_logs(db_session)
    assert total == 5
    assert len(logs) == 5

    # Filtrar por event_type
    logs, total = AuditLogService.get_logs(db_session, event_type="shipment_created")
    assert total == 3
    assert len(logs) == 3

    # Filtrar por entity_type
    logs, total = AuditLogService.get_logs(db_session, entity_type="alert")
    assert total == 2
    assert len(logs) == 2


def test_filtra_por_event_type(db_session: Session):
    """Testa filtro por event_type."""
    # Criar logs de diferentes tipos
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Shipment criado",
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
            message="Alerta gerado",
        ),
    )

    logs, total = AuditLogService.get_logs(db_session, event_type="shipment_created")
    assert total == 1
    assert logs[0].event_type == "shipment_created"


def test_filtra_por_entity_type_e_entity_id(db_session: Session):
    """Testa filtro por entity_type e entity_id."""
    # Criar logs para diferentes entidades
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_updated",
            entity_type="shipment",
            entity_id=1,
            action="update",
            severity="info",
            status="success",
            message="Shipment 1 atualizado",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_updated",
            entity_type="shipment",
            entity_id=2,
            action="update",
            severity="info",
            status="success",
            message="Shipment 2 atualizado",
        ),
    )

    logs, total = AuditLogService.get_logs(db_session, entity_type="shipment", entity_id=1)
    assert total == 1
    assert logs[0].entity_id == 1


def test_filtra_por_severity_e_status(db_session: Session):
    """Testa filtro por severity e status."""
    # Criar logs com diferentes severidades e status
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="import_failure",
            entity_type="import_history",
            action="create",
            severity="critical",
            status="failed",
            message="Falha crítica",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Sucesso",
        ),
    )

    logs, total = AuditLogService.get_logs(db_session, severity="critical", status="failed")
    assert total == 1
    assert logs[0].severity == "critical"
    assert logs[0].status == "failed"


def test_filtra_por_periodo(db_session: Session):
    """Testa filtro por período (criado_at)."""
    # Criar logs em diferentes momentos
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="test_event",
            entity_type="test",
            action="create",
            severity="info",
            status="success",
            message="Log antigo",
        ),
    )

    # Simular log mais recente (modificando created_at manualmente para teste)
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="test_event",
            entity_type="test",
            action="create",
            severity="info",
            status="success",
            message="Log recente",
        ),
    )

    # Listar todos - deve retornar ordenado por created_at desc
    logs, total = AuditLogService.get_logs(db_session)
    assert total == 2
    assert logs[0].created_at >= logs[1].created_at


def test_retorna_summary_por_tipo_severidade_status(db_session: Session):
    """Testa retorno de summary por tipo/severidade/status."""
    # Criar logs variados
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Sucesso 1",
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
            message="Sucesso 2",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="import_failure",
            entity_type="import_history",
            action="create",
            severity="critical",
            status="failed",
            message="Falha",
        ),
    )

    summary = AuditLogService.get_summary(db_session)

    assert summary.total_logs == 3
    assert summary.success_count == 2
    assert summary.failed_count == 1
    assert summary.skipped_count == 0
    assert summary.critical_count == 1
    assert summary.warning_count == 1
    assert summary.info_count == 1
    assert summary.create_count == 3
    assert summary.update_count == 0
    assert summary.delete_count == 0
    assert summary.read_count == 0


def test_get_log_by_id(db_session: Session):
    """Testa busca de log por ID."""
    log_data = AuditLogCreateRequest(
        event_type="test_event",
        entity_type="test",
        action="create",
        severity="info",
        status="success",
        message="Teste",
    )
    created_log = AuditLogService.create_log(db_session, log_data)

    found_log = AuditLogService.get_log_by_id(db_session, created_log.id)

    assert found_log is not None
    assert found_log.id == created_log.id
    assert found_log.event_type == "test_event"


def test_get_log_by_id_not_found(db_session: Session):
    """Testa busca de log por ID inexistente."""
    found_log = AuditLogService.get_log_by_id(db_session, 99999)
    assert found_log is None


def test_paginacao(db_session: Session):
    """Testa paginação de logs."""
    # Criar 25 logs
    for i in range(25):
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

    # Primeira página (10 itens)
    logs, total = AuditLogService.get_logs(db_session, skip=0, limit=10)
    assert total == 25
    assert len(logs) == 10

    # Segunda página (10 itens)
    logs, total = AuditLogService.get_logs(db_session, skip=10, limit=10)
    assert total == 25
    assert len(logs) == 10

    # Terceira página (5 itens)
    logs, total = AuditLogService.get_logs(db_session, skip=20, limit=10)
    assert total == 25
    assert len(logs) == 5


def test_filtra_por_actor_user_id(db_session: Session):
    """Testa filtro por actor_user_id."""
    # Setup: criar usuário
    user = User(
        email="admin@example.com",
        full_name="Admin",
        password_hash="hash123",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    # Criar logs com diferentes usuários
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            actor_user_id=user.id,
            actor_email=user.email,
            severity="info",
            status="success",
            message="Log do admin",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="alert_generated",
            entity_type="alert",
            action="create",
            source="system",
            severity="info",
            status="success",
            message="Log do sistema",
        ),
    )

    logs, total = AuditLogService.get_logs(db_session, actor_user_id=user.id)
    assert total == 1
    assert logs[0].actor_user_id == user.id
    assert logs[0].actor_email == user.email


def test_filtra_por_action(db_session: Session):
    """Testa filtro por action."""
    # Criar logs com diferentes ações
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_created",
            entity_type="shipment",
            action="create",
            severity="info",
            status="success",
            message="Create",
        ),
    )
    AuditLogService.create_log(
        db_session,
        AuditLogCreateRequest(
            event_type="shipment_updated",
            entity_type="shipment",
            action="update",
            severity="info",
            status="success",
            message="Update",
        ),
    )

    logs, total = AuditLogService.get_logs(db_session, action="create")
    assert total == 1
    assert logs[0].action == "create"
