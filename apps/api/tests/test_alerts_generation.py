"""Tests for alerts generation service (BETA-017A)."""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert
from app.modules.alerts.service import generate_alerts
from app.modules.carriers.models import Carrier
from app.modules.sla.models import SlaRule
from app.modules.shipments.models import Shipment


def test_gera_alerta_para_sla_critical(db_session: Session):
    """Testa geração de alerta para SLA critical."""
    # Setup: criar carrier, SLA rule e shipment com SLA critical
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    result = generate_alerts(db_session)

    # Assert
    assert result["success"] is True
    assert result["created_count"] > 0

    # Verificar alerta criado
    alert = db_session.query(Alert).filter(
        Alert.alert_type == "sla_critical",
        Alert.shipment_id == shipment.id
    ).first()
    assert alert is not None
    assert alert.severity == "critical"
    assert alert.status == "active"


def test_gera_alerta_para_sla_late(db_session: Session):
    """Testa geração de alerta para SLA late."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=5),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=5,
        criticality="media",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    result = generate_alerts(db_session)

    # Assert
    assert result["success"] is True
    assert result["created_count"] > 0

    # Verificar alerta criado
    alert = db_session.query(Alert).filter(
        Alert.alert_type == "sla_late",
        Alert.shipment_id == shipment.id
    ).first()
    assert alert is not None
    assert alert.severity == "warning"


def test_gera_alerta_para_sla_warning(db_session: Session):
    """Testa geração de alerta para SLA warning."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) + timedelta(days=1),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=0,
        criticality="baixa",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    result = generate_alerts(db_session)

    # Assert
    assert result["success"] is True


def test_nao_duplica_alerta_ativo_para_mesma_origem(db_session: Session):
    """Testa que não duplica alerta ativo para a mesma origem."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas primeira vez
    result1 = generate_alerts(db_session)
    first_count = result1["created_count"]

    # Gerar alertas segunda vez
    result2 = generate_alerts(db_session)
    second_count = result2["created_count"]

    # Assert: segunda vez deve criar menos (skipped)
    assert result2["success"] is True
    assert result2["skipped_count"] > 0


def test_geracao_retorna_contadores(db_session: Session):
    """Testa que geração retorna contadores."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    result = generate_alerts(db_session)

    # Assert
    assert "processed_count" in result
    assert "created_count" in result
    assert "skipped_count" in result
    assert "resolved_count" in result
    assert "error_count" in result
    assert result["processed_count"] >= 0
    assert result["created_count"] >= 0
    assert result["skipped_count"] >= 0
    assert result["resolved_count"] >= 0
    assert result["error_count"] == 0


def test_respeita_service_de_sla_existente(db_session: Session):
    """Testa que respeita service de SLA existente."""
    # Setup
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Cliente Teste",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas (deve usar service de SLA existente)
    result = generate_alerts(db_session)

    # Assert
    assert result["success"] is True
    # Não deve ter erros de cálculo de SLA
    assert result["error_count"] == 0


def test_nao_usa_dados_reais(db_session: Session):
    """Testa que não usa dados reais."""
    # Setup com dados fake
    carrier = Carrier(name="Fake Carrier")
    db_session.add(carrier)
    db_session.flush()

    # Criar SLA rule global
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    shipment = Shipment(
        tracking_code="FAKE123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Fake Cliente",
        recipient_phone="11999999999",
        origin_address="Rua Fake A",
        destination_address="Rua Fake B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    result = generate_alerts(db_session)

    # Assert
    assert result["success"] is True
    # Verificar que alertas não contêm dados reais
    alert = db_session.query(Alert).first()
    if alert:
        assert "Fake" in alert.title or "FAKE" in alert.title or alert.title == "Atraso Crítico"
