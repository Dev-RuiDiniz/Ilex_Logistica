"""Tests for Alert model (BETA-017A)."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment


def test_cria_alerta_valido(db_session: Session):
    """Testa criação de alerta válido."""
    # Setup: criar carrier e shipment
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
    )
    db_session.add(shipment)
    db_session.flush()

    # Criar alerta
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Atraso Crítico",
        message="Entrega com atraso crítico de 15 dias",
        source_type="shipment",
        source_id=shipment.id,
        shipment_id=shipment.id,
        carrier_id=carrier.id,
    )
    db_session.add(alert)
    db_session.commit()

    # Assert
    assert alert.id is not None
    assert alert.alert_type == "sla_critical"
    assert alert.severity == "critical"
    assert alert.title == "Atraso Crítico"
    assert alert.status == "active"
    assert alert.is_read is False
    assert alert.is_resolved is False
    assert alert.shipment_id == shipment.id
    assert alert.carrier_id == carrier.id


def test_valida_alert_type(db_session: Session):
    """Testa validação de alert_type."""
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

    assert alert.alert_type in [
        "sla_critical",
        "sla_late",
        "sla_warning",
        "unknown_sla",
        "import_failure",
    ]


def test_valida_severity(db_session: Session):
    """Testa validação de severity."""
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

    assert alert.severity in ["info", "warning", "critical"]


def test_valida_status(db_session: Session):
    """Testa validação de status."""
    alert = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Teste",
        message="Mensagem",
        source_type="shipment",
        source_id=1,
        status="active",
    )
    db_session.add(alert)
    db_session.commit()

    assert alert.status in ["active", "read", "resolved", "dismissed"]


def test_cria_alerta_associado_a_shipment(db_session: Session):
    """Testa criação de alerta associado a shipment."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
    )
    db_session.add(shipment)
    db_session.flush()

    # Criar alerta
    alert = Alert(
        alert_type="sla_late",
        severity="warning",
        title="Atraso",
        message="Entrega atrasada",
        source_type="shipment",
        source_id=shipment.id,
        shipment_id=shipment.id,
    )
    db_session.add(alert)
    db_session.commit()

    # Assert
    assert alert.shipment_id == shipment.id
    assert alert.source_id == shipment.id


def test_evita_campos_obrigatorios_ausentes(db_session: Session):
    """Testa que campos obrigatórios não podem ser nulos."""
    from sqlalchemy.exc import IntegrityError

    # Tentar criar alerta sem campos obrigatórios
    alert = Alert()
    db_session.add(alert)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_status_default_active(db_session: Session):
    """Testa que status default é active."""
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

    assert alert.status == "active"


def test_is_read_default_false(db_session: Session):
    """Testa que is_read default é False."""
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

    assert alert.is_read is False


def test_is_resolved_default_false(db_session: Session):
    """Testa que is_resolved default é False."""
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

    assert alert.is_resolved is False
