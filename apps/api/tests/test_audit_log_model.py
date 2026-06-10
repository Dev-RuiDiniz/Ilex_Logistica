"""Tests for OperationalAuditLog model (BETA-019A)."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.modules.audit.models import OperationalAuditLog
from app.modules.users.models import User


def test_cria_audit_log_valido(db_session: Session):
    """Testa criação de audit log válido."""
    # Setup: criar usuário
    user = User(
        email="teste@example.com",
        full_name="Usuário Teste",
        password_hash="hash123",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    # Criar audit log
    audit_log = OperationalAuditLog(
        event_type="shipment_created",
        entity_type="shipment",
        entity_id=1,
        action="create",
        actor_user_id=user.id,
        actor_email=user.email,
        source="api",
        severity="info",
        status="success",
        message="Shipment criado via API",
        metadata_json='{"tracking_code": "TEST123"}',
    )
    db_session.add(audit_log)
    db_session.commit()

    # Assert
    assert audit_log.id is not None
    assert audit_log.event_type == "shipment_created"
    assert audit_log.entity_type == "shipment"
    assert audit_log.entity_id == 1
    assert audit_log.action == "create"
    assert audit_log.actor_user_id == user.id
    assert audit_log.actor_email == user.email
    assert audit_log.source == "api"
    assert audit_log.severity == "info"
    assert audit_log.status == "success"
    assert audit_log.message == "Shipment criado via API"
    assert audit_log.metadata_json == '{"tracking_code": "TEST123"}'
    assert audit_log.created_at is not None


def test_valida_event_type(db_session: Session):
    """Testa validação de event_type."""
    audit_log = OperationalAuditLog(
        event_type="shipment_created",
        entity_type="shipment",
        action="create",
        severity="info",
        status="success",
        message="Teste",
    )
    db_session.add(audit_log)
    db_session.commit()

    valid_event_types = [
        "shipment_created",
        "shipment_updated",
        "shipment_imported",
        "import_previewed",
        "import_confirmed",
        "sla_recalculated",
        "sla_rule_changed",
        "alert_generated",
        "alert_read",
        "alert_resolved",
        "daily_report_generated",
        "exception_viewed",
    ]
    assert audit_log.event_type in valid_event_types


def test_valida_severity(db_session: Session):
    """Testa validação de severity."""
    audit_log = OperationalAuditLog(
        event_type="shipment_created",
        entity_type="shipment",
        action="create",
        severity="warning",
        status="success",
        message="Teste",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.severity in ["info", "warning", "critical"]


def test_valida_status(db_session: Session):
    """Testa validação de status."""
    audit_log = OperationalAuditLog(
        event_type="shipment_created",
        entity_type="shipment",
        action="create",
        severity="info",
        status="failed",
        message="Teste",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.status in ["success", "failed", "skipped"]


def test_aceita_metadata_json(db_session: Session):
    """Testa que aceita metadata_json."""
    audit_log = OperationalAuditLog(
        event_type="shipment_created",
        entity_type="shipment",
        action="create",
        severity="info",
        status="success",
        message="Teste",
        metadata_json='{"key": "value", "number": 123}',
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.metadata_json == '{"key": "value", "number": 123}'


def test_aceita_before_json(db_session: Session):
    """Testa que aceita before_json."""
    audit_log = OperationalAuditLog(
        event_type="shipment_updated",
        entity_type="shipment",
        action="update",
        severity="info",
        status="success",
        message="Teste",
        before_json='{"status": "pending"}',
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.before_json == '{"status": "pending"}'


def test_aceita_after_json(db_session: Session):
    """Testa que aceita after_json."""
    audit_log = OperationalAuditLog(
        event_type="shipment_updated",
        entity_type="shipment",
        action="update",
        severity="info",
        status="success",
        message="Teste",
        after_json='{"status": "in_transit"}',
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.after_json == '{"status": "in_transit"}'


def test_nao_exige_usuario_quando_evento_sistemico(db_session: Session):
    """Testa que não exige usuário quando evento é sistêmico."""
    audit_log = OperationalAuditLog(
        event_type="alert_generated",
        entity_type="alert",
        action="create",
        source="system",
        severity="info",
        status="success",
        message="Alerta gerado automaticamente pelo sistema",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.actor_user_id is None
    assert audit_log.actor_email is None
    assert audit_log.source == "system"


def test_evita_campos_obrigatorios_ausentes(db_session: Session):
    """Testa que campos obrigatórios não podem ser nulos."""
    from sqlalchemy.exc import IntegrityError

    # Tentar criar audit log sem campos obrigatórios
    audit_log = OperationalAuditLog()
    db_session.add(audit_log)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_cria_audit_log_com_usuario(db_session: Session):
    """Testa criação de audit log com usuário associado."""
    # Setup: criar usuário
    user = User(
        email="admin@example.com",
        full_name="Admin",
        password_hash="hash123",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    # Criar audit log
    audit_log = OperationalAuditLog(
        event_type="sla_rule_changed",
        entity_type="sla_rule",
        entity_id=1,
        action="update",
        actor_user_id=user.id,
        actor_email=user.email,
        source="api",
        severity="warning",
        status="success",
        message="Regra SLA alterada por admin",
    )
    db_session.add(audit_log)
    db_session.commit()

    # Assert
    assert audit_log.actor_user_id == user.id
    assert audit_log.actor_email == user.email


def test_cria_audit_log_com_request_id(db_session: Session):
    """Testa criação de audit log com request_id para correlação."""
    audit_log = OperationalAuditLog(
        event_type="import_confirmed",
        entity_type="import_history",
        entity_id=1,
        action="create",
        source="api",
        severity="info",
        status="success",
        message="Importação confirmada",
        request_id="req-abc-123",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.request_id == "req-abc-123"


def test_cria_audit_log_com_ip_address(db_session: Session):
    """Testa criação de audit log com ip_address."""
    audit_log = OperationalAuditLog(
        event_type="user_login",
        entity_type="user",
        entity_id=1,
        action="read",
        source="api",
        severity="info",
        status="success",
        message="Login realizado",
        ip_address="192.168.1.1",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.ip_address == "192.168.1.1"


def test_cria_audit_log_com_user_agent(db_session: Session):
    """Testa criação de audit log com user_agent."""
    audit_log = OperationalAuditLog(
        event_type="user_login",
        entity_type="user",
        entity_id=1,
        action="read",
        source="api",
        severity="info",
        status="success",
        message="Login realizado",
        user_agent="Mozilla/5.0",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.user_agent == "Mozilla/5.0"


def test_cria_audit_log_com_antes_e_depois(db_session: Session):
    """Testa criação de audit log com before_json e after_json."""
    audit_log = OperationalAuditLog(
        event_type="shipment_updated",
        entity_type="shipment",
        entity_id=1,
        action="update",
        source="api",
        severity="info",
        status="success",
        message="Status atualizado",
        before_json='{"status": "pending", "delay_days": 0}',
        after_json='{"status": "in_transit", "delay_days": 1}',
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.before_json == '{"status": "pending", "delay_days": 0}'
    assert audit_log.after_json == '{"status": "in_transit", "delay_days": 1}'


def test_cria_audit_log_critical_severity(db_session: Session):
    """Testa criação de audit log com severity critical."""
    audit_log = OperationalAuditLog(
        event_type="import_failure",
        entity_type="import_history",
        entity_id=1,
        action="create",
        source="system",
        severity="critical",
        status="failed",
        message="Falha crítica na importação",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.severity == "critical"
    assert audit_log.status == "failed"


def test_cria_audit_log_skipped_status(db_session: Session):
    """Testa criação de audit log com status skipped."""
    audit_log = OperationalAuditLog(
        event_type="sla_recalculated",
        entity_type="shipment",
        entity_id=1,
        action="update",
        source="system",
        severity="info",
        status="skipped",
        message="SLA não recalculado (sem mudanças)",
    )
    db_session.add(audit_log)
    db_session.commit()

    assert audit_log.status == "skipped"
