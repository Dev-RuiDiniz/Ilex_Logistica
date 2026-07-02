"""Tests for alerts generation service (BETA-017A)."""

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.modules.alerts.models import Alert, AlertDeliveryLog
from app.modules.alerts.service import (
    generate_alerts,
    get_no_update_alert_count,
    mark_alert_as_read,
    mark_alert_as_resolved,
)
from app.modules.carriers.models import Carrier
from app.modules.imports.models import ImportHistory
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


def test_regeracao_contabiliza_alerta_ativo_como_ignorado(db_session: Session):
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
    result1["created_count"]

    # Gerar alertas segunda vez
    result2 = generate_alerts(db_session)
    result2["created_count"]

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


def _seed_sla_rule(db_session: Session) -> None:
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()


def _seed_carrier(db_session: Session, name: str = "Transportadora Teste") -> Carrier:
    carrier = Carrier(name=name)
    db_session.add(carrier)
    db_session.flush()
    return carrier


def test_gera_alerta_de_falha_de_importacao_e_registra_log(db_session: Session):
    """Falhas de importação devem gerar alerta e log de entrega."""
    history = ImportHistory(
        filename="falha.csv",
        file_type="csv",
        file_hash="hash-falha-001",
        rows_received=5,
        duplicates_count=1,
        imported_count=0,
        rejected_count=4,
        status="failed",
        imported_by=1,
    )
    db_session.add(history)
    db_session.commit()

    result = generate_alerts(db_session)

    assert result["success"] is True
    assert result["created_count"] == 1
    assert result["error_count"] == 0

    alert = (
        db_session.query(Alert)
        .filter(Alert.alert_type == "import_failure", Alert.source_type == "import", Alert.source_id == history.id)
        .one()
    )
    assert alert.severity == "critical"
    assert alert.is_resolved is False

    log = (
        db_session.query(AlertDeliveryLog)
        .filter(AlertDeliveryLog.alert_id == alert.id)
        .one()
    )
    assert log.event_type == "generated"
    assert log.source_type == "import"
    assert log.alert_type == "import_failure"


def test_gera_alerta_no_update_e_resolve_quando_atualiza(db_session: Session):
    """Shipments sem atualização devem gerar alerta e ser resolvidos quando voltam a atualizar."""
    carrier = _seed_carrier(db_session)
    _seed_sla_rule(db_session)

    now = datetime.now(UTC)
    shipment = Shipment(
        tracking_code="STALE001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now + timedelta(days=3),
        actual_delivery=None,
        recipient_name="Cliente Estagnado",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        customer_name="Cliente Estagnado",
        destination_uf="SP",
        invoice_number="NF-STALE-1",
        freight_value=10.00,
        invoice_value=100.00,
        updated_at=now - timedelta(days=8),
        criticality="normal",
    )
    db_session.add(shipment)
    db_session.commit()

    first_result = generate_alerts(db_session)
    assert first_result["success"] is True
    assert first_result["created_count"] == 1
    assert get_no_update_alert_count(db_session) == 1

    alert = (
        db_session.query(Alert)
        .filter(Alert.alert_type == "no_update", Alert.source_type == "shipment", Alert.source_id == shipment.id)
        .one()
    )
    assert alert.severity == "warning"

    shipment.updated_at = now
    db_session.commit()

    second_result = generate_alerts(db_session)
    assert second_result["success"] is True
    assert second_result["resolved_count"] >= 1
    assert get_no_update_alert_count(db_session) == 0

    alert_after = db_session.query(Alert).filter(Alert.id == alert.id).one()
    assert alert_after.is_resolved is True
    assert alert_after.status == "resolved"

    auto_resolved_log = (
        db_session.query(AlertDeliveryLog)
        .filter(AlertDeliveryLog.alert_id == alert.id, AlertDeliveryLog.event_type == "auto_resolved")
        .one()
    )
    assert auto_resolved_log.source_type == "shipment"


def test_nao_duplica_alerta_ativo_para_mesma_origem(db_session: Session):
    """Regerar alertas não deve duplicar o alerta ativo para a mesma origem."""
    carrier = _seed_carrier(db_session)
    _seed_sla_rule(db_session)

    now = datetime.now(UTC)
    shipment = Shipment(
        tracking_code="CRIT-001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=15),
        actual_delivery=None,
        recipient_name="Cliente Crítico",
        recipient_phone="11999999999",
        origin_address="Rua C",
        destination_address="Rua D",
        customer_name="Cliente Crítico",
        destination_uf="RJ",
        invoice_number="NF-CRIT-1",
        freight_value=12.50,
        invoice_value=125.00,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    first_result = generate_alerts(db_session)
    second_result = generate_alerts(db_session)

    assert first_result["created_count"] == 1
    assert second_result["created_count"] == 0
    assert second_result["skipped_count"] >= 1

    active_alerts = (
        db_session.query(Alert)
        .filter(
            Alert.source_type == "shipment",
            Alert.source_id == shipment.id,
            Alert.status == "active",
            Alert.is_resolved.is_(False),
        )
        .all()
    )
    assert len(active_alerts) == 1

    skipped_logs = (
        db_session.query(AlertDeliveryLog)
        .filter(
            AlertDeliveryLog.source_type == "shipment",
            AlertDeliveryLog.source_id == shipment.id,
            AlertDeliveryLog.event_type == "skipped_duplicate",
        )
        .count()
    )
    assert skipped_logs >= 1


def test_marcar_alerta_como_lida_e_resolvida_registra_logs(db_session: Session):
    """Marcar um alerta como lido e resolvido deve registrar os eventos."""
    carrier = _seed_carrier(db_session)
    _seed_sla_rule(db_session)

    now = datetime.now(UTC)
    shipment = Shipment(
        tracking_code="READ-001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=20),
        actual_delivery=None,
        recipient_name="Cliente Leitura",
        recipient_phone="11999999999",
        origin_address="Rua E",
        destination_address="Rua F",
        customer_name="Cliente Leitura",
        destination_uf="MG",
        invoice_number="NF-READ-1",
        freight_value=18.00,
        invoice_value=180.00,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    generate_alerts(db_session)
    alert = db_session.query(Alert).filter(Alert.source_type == "shipment", Alert.source_id == shipment.id).one()

    mark_alert_as_read(db_session, alert.id)
    mark_alert_as_resolved(db_session, alert.id)

    refreshed = db_session.query(Alert).filter(Alert.id == alert.id).one()
    assert refreshed.is_read is True
    assert refreshed.is_resolved is True
    assert refreshed.status == "resolved"

    event_types = [
        log.event_type
        for log in db_session.query(AlertDeliveryLog)
        .filter(AlertDeliveryLog.alert_id == alert.id)
        .order_by(AlertDeliveryLog.id.asc())
        .all()
    ]
    assert "read" in event_types
    assert "resolved" in event_types
