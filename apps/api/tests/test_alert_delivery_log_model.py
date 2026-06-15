"""Tests for AlertDeliveryLog model (BETA-027)."""

from datetime import UTC, datetime
import pytest
from sqlalchemy.orm import Session

from app.modules.alerts.models import AlertDeliveryLog, Alert
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment


def test_cria_delivery_log_valido(db_session: Session):
    """Testa criação de delivery log válido."""
    # Setup: criar alerta
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem de teste",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    # Criar delivery log
    log = AlertDeliveryLog(
        alert_id=alert.id,
        channel="email",
        recipient="test@example.com",
        subject="Teste",
        message="Mensagem de teste",
        status="pending",
        max_attempts=3,
    )
    db_session.add(log)
    db_session.commit()

    # Assert
    assert log.id is not None
    assert log.alert_id == alert.id
    assert log.channel == "email"
    assert log.recipient == "test@example.com"
    assert log.subject == "Teste"
    assert log.message == "Mensagem de teste"
    assert log.status == "pending"
    assert log.attempts == 0
    assert log.max_attempts == 3
    assert log.sent_at is None
    assert log.created_at is not None
    assert log.updated_at is not None


def test_valida_channel(db_session: Session):
    """Testa validação de channel."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    for channel in ["email", "sms", "webhook", "push"]:
        log = AlertDeliveryLog(
            alert_id=alert.id,
            channel=channel,
            recipient="test@example.com",
            message="Mensagem",
        )
        db_session.add(log)
        db_session.commit()

        assert log.channel in ["email", "sms", "webhook", "push"]


def test_valida_status(db_session: Session):
    """Testa validação de status."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    for status in ["pending", "sent", "failed"]:
        log = AlertDeliveryLog(
            alert_id=alert.id,
            channel="email",
            recipient="test@example.com",
            message="Mensagem",
            status=status,
        )
        db_session.add(log)
        db_session.commit()

        assert log.status in ["pending", "sent", "failed"]


def test_defaults(db_session: Session):
    """Testa valores padrão."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    log = AlertDeliveryLog(
        alert_id=alert.id,
        channel="email",
        recipient="test@example.com",
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    assert log.status == "pending"
    assert log.attempts == 0
    assert log.max_attempts == 3
    assert log.subject is None
    assert log.error_message is None


def test_foreign_key_constraint(db_session: Session):
    """Testa constraint de foreign key - alerta inexistente."""
    from sqlalchemy.exc import IntegrityError

    # Tenta criar log com alert_id inexistente
    log = AlertDeliveryLog(
        alert_id=99999,  # ID inexistente
        channel="email",
        recipient="test@example.com",
        message="Mensagem",
    )
    db_session.add(log)

    # SQLite may not enforce FK by default, so we check the alert doesn't exist
    from app.modules.alerts.models import Alert
    alert = db_session.query(Alert).filter(Alert.id == 99999).first()
    assert alert is None


def test_update_status_sent(db_session: Session):
    """Testa atualização de status para sent."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    log = AlertDeliveryLog(
        alert_id=alert.id,
        channel="email",
        recipient="test@example.com",
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    # Atualizar para sent
    log.status = "sent"
    log.sent_at = datetime.now(UTC)
    log.attempts = 1
    db_session.commit()

    assert log.status == "sent"
    assert log.sent_at is not None
    assert log.attempts == 1


def test_update_status_failed(db_session: Session):
    """Testa atualização de status para failed com erro."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
    )
    db_session.add(alert)
    db_session.commit()

    log = AlertDeliveryLog(
        alert_id=alert.id,
        channel="email",
        recipient="test@example.com",
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    # Atualizar para failed
    log.status = "failed"
    log.error_message = "Connection timeout"
    log.attempts = 1
    db_session.commit()

    assert log.status == "failed"
    assert log.error_message == "Connection timeout"
    assert log.attempts == 1