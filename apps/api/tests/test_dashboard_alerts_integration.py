"""Tests for dashboard alerts integration (BETA-017A)."""

from sqlalchemy.orm import Session


def test_dashboard_summary_retorna_active_alerts_count_real(db_session: Session):
    """Testa dashboard summary retorna active_alerts_count real."""
    from app.modules.dashboard.service import calculate_dashboard_summary
    from app.modules.alerts.models import Alert
    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment
    from app.modules.sla.models import SlaRule
    from datetime import UTC, datetime, timedelta

    # Setup: criar SLA rule
    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    # Setup: criar carrier e shipment
    carrier = Carrier(name="Test Carrier")
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC) - timedelta(days=20),
        recipient_name="Test",
        recipient_phone="11999999999",
        origin_address="A",
        destination_address="B",
        delay_days=20,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    # Gerar alertas
    from app.modules.alerts.service import generate_alerts
    generate_alerts(db_session)

    # Calcular dashboard summary
    result = calculate_dashboard_summary(db_session)

    # Assert: active_alerts_count deve ser real
    assert result["active_alerts_count"] >= 0
    # Se houver alertas, deve contar
    alert_count = db_session.query(Alert).filter(
        Alert.status == "active",
        Alert.is_resolved.is_(False)
    ).count()
    assert result["active_alerts_count"] == alert_count


def test_active_alerts_count_ignora_resolvidos(db_session: Session):
    """Testa active_alerts_count ignora resolvidos."""
    from app.modules.alerts.service import get_active_alerts_count
    from app.modules.alerts.models import Alert
    from app.modules.carriers.models import Carrier
    from app.modules.shipments.models import Shipment
    from datetime import UTC, datetime

    # Setup: criar carrier e shipment
    carrier = Carrier(name="Test Carrier")
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test",
        recipient_phone="11999999999",
        origin_address="A",
        destination_address="B",
    )
    db_session.add(shipment)
    db_session.flush()

    # Criar alerta resolvido
    alert_resolved = Alert(
        alert_type="sla_critical",
        severity="critical",
        title="Test",
        message="Test message",
        source_type="shipment",
        source_id=shipment.id,
        shipment_id=shipment.id,
        carrier_id=carrier.id,
        status="resolved",
        is_resolved=True,
    )
    db_session.add(alert_resolved)

    # Criar alerta ativo
    alert_active = Alert(
        alert_type="sla_late",
        severity="warning",
        title="Test",
        message="Test message",
        source_type="shipment",
        source_id=shipment.id,
        shipment_id=shipment.id,
        carrier_id=carrier.id,
        status="active",
        is_resolved=False,
    )
    db_session.add(alert_active)
    db_session.commit()

    # Contar alertas ativos
    active_count = get_active_alerts_count(db_session)

    # Assert: deve contar apenas ativos
    assert active_count == 1


def test_dashboard_mantem_payload_estavel(db_session: Session):
    """Testa dashboard mantém payload estável."""
    from app.modules.dashboard.service import calculate_dashboard_summary

    result = calculate_dashboard_summary(db_session)

    # Verificar campos esperados
    assert "total_shipments" in result
    assert "on_time_count" in result
    assert "late_count" in result
    assert "critical_count" in result
    assert "warning_count" in result
    assert "unknown_sla_count" in result
    assert "exceptions_count" in result
    assert "import_failure_count" in result
    assert "active_alerts_count" in result
    assert "carriers_count" in result
    assert "top_carriers_by_efficiency" in result
    assert "top_exceptions" in result
    assert "generated_at" in result
    assert "filters_applied" in result
