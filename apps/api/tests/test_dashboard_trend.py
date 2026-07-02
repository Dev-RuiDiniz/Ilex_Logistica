"""Tests for dashboard trend endpoint for BETA-029."""

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.modules.dashboard.service import calculate_dashboard_trend
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment


def test_calcula_tendencia_diaria(db_session: Session):
    """Testa cálculo de tendência diária dos KPIs."""
    # Setup: criar carrier
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=7)

    # Criar shipments em dias diferentes
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TEST{i:03d}",
            carrier_id=carrier.id,
            status="in_transit",
            estimated_delivery=end_date - timedelta(days=i),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)
    db_session.commit()

    # Calcular tendência
    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    assert "trend_data" in result
    assert "period" in result
    assert len(result["trend_data"]) == 8  # 7 dias + 1 = 8 dias
    assert result["period"]["days"] == 8


def test_calcula_tendencia_com_dados_vazios(db_session: Session):
    """Testa tendência quando não há shipments no período."""
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=7)

    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    assert "trend_data" in result
    assert len(result["trend_data"]) == 8
    # Todos os contadores devem ser 0
    for day_data in result["trend_data"]:
        assert day_data["total_shipments"] == 0
        assert day_data["on_time_count"] == 0
        assert day_data["late_count"] == 0
        assert day_data["critical_count"] == 0
        assert day_data["warning_count"] == 0
        assert day_data["unknown_sla_count"] == 0
        assert day_data["exceptions_count"] == 0


def test_calcula_tendencia_respeita_periodo_customizado(db_session: Session):
    """Testa que tendência respeita período customizado (ex: 14 dias)."""
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=14)

    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    assert result["period"]["days"] == 15  # 14 + 1


def test_calcula_tendencia_limita_maximo_90_dias(db_session: Session):
    """Testa que tendência limita a 90 dias máximo."""
    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=120)

    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    assert result["period"]["days"] <= 91  # 90 + 1


def test_calcula_tendencia_inverte_datas_se_necessario(db_session: Session):
    """Testa que inverte datas se start > end."""
    end_date = datetime.now(UTC)
    start_date = end_date + timedelta(days=10)  # start no futuro

    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    # Deve inverter e funcionar
    assert result["period"]["days"] > 0


def test_tendencia_inclui_contadores_sla_corretos(db_session: Session):
    """Testa que contadores SLA estão corretos na tendência."""
    carrier = Carrier(name="Transportadora Teste")
    db_session.add(carrier)
    db_session.flush()

    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=1)

    # Criar 2 shipments no mesmo dia
    for i in range(2):
        shipment = Shipment(
            tracking_code=f"TEST{i:03d}",
            carrier_id=carrier.id,
            status="in_transit",
            estimated_delivery=end_date - timedelta(days=1),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A",
            destination_address="Rua B",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)
    db_session.commit()

    result = calculate_dashboard_trend(
        db_session,
        estimated_delivery_from=start_date.date().isoformat(),
        estimated_delivery_to=end_date.date().isoformat(),
    )

    # Encontrar o dia do dia anterior
    yesterday_key = (end_date - timedelta(days=1)).date().isoformat()
    day_data = next((d for d in result["trend_data"] if d["date"] == yesterday_key), None)

    assert day_data is not None
    assert day_data["total_shipments"] == 2
    assert day_data["on_time_count"] + day_data["late_count"] + day_data["critical_count"] + day_data["warning_count"] + day_data["unknown_sla_count"] == 2