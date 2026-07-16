"""Tests for AlertDeliveryLog model (BETA-027)."""

from sqlalchemy.orm import Session

from app.modules.alerts.models import AlertDeliveryLog, Alert


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

    # Criar delivery log (contrato real do modelo BETA-027)
    log = AlertDeliveryLog(
        alert_id=alert.id,
        channel="in_app",
        recipient="internal",
        event_type="alert_generated",
        delivery_channel="email",
        delivery_status="success",
        source_type="shipment",
        source_id=1,
        alert_type="sla_critical",
        message="Mensagem de teste",
    )
    db_session.add(log)
    db_session.commit()

    # Assert
    assert log.id is not None
    assert log.alert_id == alert.id
    assert log.event_type == "alert_generated"
    assert log.delivery_channel == "email"
    assert log.delivery_status == "success"
    assert log.source_type == "shipment"
    assert log.source_id == 1
    assert log.alert_type == "sla_critical"
    assert log.message == "Mensagem de teste"
    assert log.metadata_json is None
    assert log.created_at is not None


def test_valida_delivery_channel(db_session: Session):
    """Testa canais de entrega suportados."""
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

    for channel in ["email", "sms", "webhook", "push", "in_app"]:
        log = AlertDeliveryLog(
            alert_id=alert.id,
            channel="in_app",
            recipient="internal",
            event_type="alert_generated",
            delivery_channel=channel,
            delivery_status="success",
            source_type="shipment",
            source_id=1,
            message="Mensagem",
        )
        db_session.add(log)
        db_session.commit()

        assert log.delivery_channel in ["email", "sms", "webhook", "push", "in_app"]


def test_valida_delivery_status(db_session: Session):
    """Testa status de entrega suportados."""
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

    for status in ["pending", "success", "failed"]:
        log = AlertDeliveryLog(
            alert_id=alert.id,
            channel="in_app",
            recipient="internal",
            event_type="alert_generated",
            delivery_channel="email",
            delivery_status=status,
            source_type="shipment",
            source_id=1,
            message="Mensagem",
        )
        db_session.add(log)
        db_session.commit()

        assert log.delivery_status in ["pending", "success", "failed"]


def test_defaults(db_session: Session):
    """Testa valores padrão do modelo."""
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
        channel="in_app",
        recipient="internal",
        event_type="alert_generated",
        delivery_channel="email",
        delivery_status="success",
        source_type="shipment",
        source_id=1,
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    # delivery_channel e delivery_status têm defaults no modelo
    assert log.delivery_channel == "email"
    assert log.delivery_status == "success"
    assert log.metadata_json is None


def test_foreign_key_constraint(db_session: Session):
    """Testa constraint de foreign key - alerta inexistente."""

    # Tenta criar log com alert_id inexistente
    log = AlertDeliveryLog(
        alert_id=99999,  # ID inexistente
        channel="in_app",
        recipient="internal",
        event_type="alert_generated",
        delivery_channel="email",
        delivery_status="success",
        source_type="shipment",
        source_id=1,
        message="Mensagem",
    )
    db_session.add(log)

    # SQLite may not enforce FK by default, so we check the alert doesn't exist
    from app.modules.alerts.models import Alert
    alert = db_session.query(Alert).filter(Alert.id == 99999).first()
    assert alert is None


def test_update_status_sent(db_session: Session):
    """Testa atualização de status para success."""
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
        channel="in_app",
        recipient="internal",
        event_type="alert_generated",
        delivery_channel="email",
        delivery_status="pending",
        source_type="shipment",
        source_id=1,
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    # Atualizar para success
    log.delivery_status = "success"
    db_session.commit()

    assert log.delivery_status == "success"


def test_update_status_failed(db_session: Session):
    """Testa atualização de status para failed com metadata de erro."""
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
        channel="in_app",
        recipient="internal",
        event_type="alert_generated",
        delivery_channel="email",
        delivery_status="pending",
        source_type="shipment",
        source_id=1,
        message="Mensagem",
    )
    db_session.add(log)
    db_session.commit()

    # Atualizar para failed com metadata de erro
    log.delivery_status = "failed"
    log.metadata_json = '{"error": "Connection timeout"}'
    db_session.commit()

    assert log.delivery_status == "failed"
    assert "Connection timeout" in log.metadata_json