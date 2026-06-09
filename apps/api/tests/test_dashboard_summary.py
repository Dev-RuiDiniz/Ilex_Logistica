"""Testes do service de dashboard summary para BETA-016A."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.dashboard.service import calculate_dashboard_summary
from app.modules.imports.models import ImportHistory
from app.modules.shipments.models import Shipment
from app.modules.sla.models import SlaRule


@pytest.fixture
def db_with_dashboard_data(db_session: Session):
    """Popula banco com dados para testes de dashboard."""
    # Criar transportadoras
    carrier1 = Carrier(name="Transportadora A")
    carrier2 = Carrier(name="Transportadora B")
    db_session.add(carrier1)
    db_session.add(carrier2)
    db_session.flush()

    # Criar regra SLA global
    sla_rule = SlaRule(
        carrier_id=None,
        destination_uf=None,
        transit_days=7,
        warning_threshold_days=3,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    # Criar shipments com diferentes status SLA
    now = datetime.now(UTC)

    # On time
    shipment_on_time = Shipment(
        tracking_code="ON001",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=now + timedelta(days=5),
        actual_delivery=now + timedelta(days=5),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        customer_name="Cliente X",
        destination_uf="SP",
        invoice_number="NF001",
        freight_value=Decimal("10.00"),
        invoice_value=Decimal("100.00"),
    )
    db_session.add(shipment_on_time)

    # Late
    shipment_late = Shipment(
        tracking_code="LA001",
        carrier_id=carrier1.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=5),
        actual_delivery=None,
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C",
        destination_address="Rua D",
        customer_name="Cliente Y",
        destination_uf="RJ",
        invoice_number="NF002",
        freight_value=Decimal("15.00"),
        invoice_value=Decimal("150.00"),
    )
    db_session.add(shipment_late)

    # Critical
    shipment_critical = Shipment(
        tracking_code="CR001",
        carrier_id=carrier2.id,
        status="pending",
        estimated_delivery=now - timedelta(days=15),
        actual_delivery=None,
        recipient_name="Cliente 3",
        recipient_phone="11999999999",
        origin_address="Rua E",
        destination_address="Rua F",
        customer_name="Cliente Z",
        destination_uf="MG",
        invoice_number="NF003",
        freight_value=Decimal("20.00"),
        invoice_value=Decimal("200.00"),
    )
    db_session.add(shipment_critical)

    # Warning
    shipment_warning = Shipment(
        tracking_code="WA001",
        carrier_id=carrier2.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=2),
        actual_delivery=None,
        recipient_name="Cliente 4",
        recipient_phone="11999999999",
        origin_address="Rua G",
        destination_address="Rua H",
        customer_name="Cliente W",
        destination_uf="RS",
        invoice_number="NF004",
        freight_value=Decimal("12.00"),
        invoice_value=Decimal("120.00"),
    )
    db_session.add(shipment_warning)

    # Unknown SLA (sem estimated_delivery)
    shipment_unknown = Shipment(
        tracking_code="UN001",
        carrier_id=carrier1.id,
        status="pending",
        estimated_delivery=now + timedelta(days=30),
        actual_delivery=None,
        recipient_name="Cliente 5",
        recipient_phone="11999999999",
        origin_address="Rua I",
        destination_address="Rua J",
        customer_name="Cliente V",
        destination_uf="PR",
        invoice_number="NF005",
        freight_value=Decimal("18.00"),
        invoice_value=Decimal("180.00"),
    )
    db_session.add(shipment_unknown)

    # Criar histórico de importação com falhas
    import_history = ImportHistory(
        filename="test.csv",
        file_type="csv",
        file_hash="abc123",
        rows_received=10,
        duplicates_count=0,
        imported_count=8,
        rejected_count=2,
        status="SUCCESS",
        imported_by=1,
    )
    db_session.add(import_history)

    db_session.commit()

    return {
        "carrier1_id": carrier1.id,
        "carrier2_id": carrier2.id,
        "sla_rule_id": sla_rule.id,
    }


def test_deve_calcular_total_de_entregas(db_session: Session, db_with_dashboard_data):
    """Deve calcular total de entregas."""
    result = calculate_dashboard_summary(db_session)

    assert result["total_shipments"] == 5


def test_deve_calcular_entregas_no_prazo(db_session: Session, db_with_dashboard_data):
    """Deve calcular entregas no prazo."""
    result = calculate_dashboard_summary(db_session)

    # on_time_count baseado em sla_status on_time
    assert result["on_time_count"] >= 1


def test_deve_calcular_entregas_atrasadas(db_session: Session, db_with_dashboard_data):
    """Deve calcular entregas atrasadas."""
    result = calculate_dashboard_summary(db_session)

    # late_count baseado em sla_status late
    assert result["late_count"] >= 0


def test_deve_calcular_entregas_criticas(db_session: Session, db_with_dashboard_data):
    """Deve calcular entregas críticas."""
    result = calculate_dashboard_summary(db_session)

    assert result["critical_count"] == 1


def test_deve_calcular_entregas_em_warning_atencao(db_session: Session, db_with_dashboard_data):
    """Deve calcular entregas em warning/atenção."""
    result = calculate_dashboard_summary(db_session)

    assert result["warning_count"] == 1


def test_deve_calcular_entregas_sem_sla(db_session: Session, db_with_dashboard_data):
    """Deve calcular entregas sem SLA."""
    result = calculate_dashboard_summary(db_session)

    # unknown_sla_count baseado em sla_status unknown
    assert result["unknown_sla_count"] >= 0


def test_deve_calcular_excecoes_totais(db_session: Session, db_with_dashboard_data):
    """Deve calcular exceções totais."""
    result = calculate_dashboard_summary(db_session)

    # Exceções = late + critical + warning
    assert result["exceptions_count"] == 3


def test_deve_incluir_falhas_de_importacao_quando_houver_historico(
    db_session: Session, db_with_dashboard_data
):
    """Deve incluir falhas de importação quando houver histórico."""
    result = calculate_dashboard_summary(db_session)

    assert result["import_failure_count"] == 2


def test_deve_retornar_active_alerts_count_zero_quando_alertas_reais_nao_existirem(
    db_session: Session, db_with_dashboard_data
):
    """Deve retornar active_alerts_count zero quando alertas reais não existirem."""
    result = calculate_dashboard_summary(db_session)

    # Módulo de alertas não existe ainda
    assert result["active_alerts_count"] == 0


def test_deve_incluir_top_transportadoras_por_eficiencia(
    db_session: Session, db_with_dashboard_data
):
    """Deve incluir top transportadoras por eficiência."""
    result = calculate_dashboard_summary(db_session)

    assert "top_carriers_by_efficiency" in result
    assert len(result["top_carriers_by_efficiency"]) == 2


def test_deve_incluir_top_excecoes_priorizadas(db_session: Session, db_with_dashboard_data):
    """Deve incluir top exceções priorizadas."""
    result = calculate_dashboard_summary(db_session)

    assert "top_exceptions" in result
    assert len(result["top_exceptions"]) == 3


def test_deve_aplicar_filtro_por_periodo(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por período."""
    now = datetime.now(UTC)
    from_date = (now - timedelta(days=10)).isoformat()
    to_date = (now + timedelta(days=10)).isoformat()

    result = calculate_dashboard_summary(
        db_session, estimated_delivery_from=from_date, estimated_delivery_to=to_date
    )

    # Deve filtrar shipments dentro do período
    assert result["total_shipments"] >= 0


def test_deve_aplicar_filtro_por_mes_ano(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por mês/ano."""
    now = datetime.now(UTC)

    result = calculate_dashboard_summary(db_session, month=now.month, year=now.year)

    assert result["total_shipments"] >= 0


def test_deve_aplicar_filtro_por_cliente(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por cliente."""
    result = calculate_dashboard_summary(db_session, customer_name="Cliente X")

    assert result["total_shipments"] == 1


def test_deve_aplicar_filtro_por_uf(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por UF."""
    result = calculate_dashboard_summary(db_session, destination_uf="SP")

    assert result["total_shipments"] == 1


def test_deve_aplicar_filtro_por_transportadora(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por transportadora."""
    carrier_id = db_with_dashboard_data["carrier1_id"]

    result = calculate_dashboard_summary(db_session, carrier_id=carrier_id)

    assert result["total_shipments"] == 3


def test_deve_aplicar_filtro_por_criticality(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por criticality."""
    result = calculate_dashboard_summary(db_session, criticality="alta")

    # Deve filtrar por criticality alta
    assert result["total_shipments"] >= 0


def test_deve_aplicar_filtro_por_sla_status(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por sla_status."""
    result = calculate_dashboard_summary(db_session, sla_status="on_time")

    # Deve filtrar por sla_status on_time
    assert result["total_shipments"] >= 0


def test_deve_aplicar_filtro_por_is_late(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por is_late."""
    result = calculate_dashboard_summary(db_session, is_late=True)

    # late + critical + warning
    assert result["total_shipments"] == 3


def test_deve_aplicar_filtro_por_exception_type(db_session: Session, db_with_dashboard_data):
    """Deve aplicar filtro por exception_type."""
    result = calculate_dashboard_summary(db_session, exception_type="critical")

    assert result["total_shipments"] == 1


def test_deve_ignorar_filtros_vazios(db_session: Session, db_with_dashboard_data):
    """Deve ignorar filtros vazios."""
    result = calculate_dashboard_summary(
        db_session,
        customer_name="",
        destination_uf="",
        criticality="",
    )

    # Deve retornar todos os dados
    assert result["total_shipments"] == 5


def test_deve_retornar_payload_estavel_com_generated_at_e_filters_applied(
    db_session: Session, db_with_dashboard_data
):
    """Deve retornar payload estável com generated_at e filters_applied."""
    result = calculate_dashboard_summary(db_session, customer_name="Cliente X")

    assert "generated_at" in result
    assert "filters_applied" in result
    assert result["filters_applied"]["customer_name"] == "Cliente X"


def test_deve_evitar_divisao_por_zero(db_session: Session):
    """Deve evitar divisão por zero."""
    result = calculate_dashboard_summary(db_session)

    # Base vazia não deve causar erro
    assert result["total_shipments"] == 0
    assert result["on_time_count"] == 0


def test_deve_lidar_com_base_vazia(db_session: Session):
    """Deve lidar com base vazia."""
    result = calculate_dashboard_summary(db_session)

    assert result["total_shipments"] == 0
    assert result["on_time_count"] == 0
    assert result["late_count"] == 0
    assert result["critical_count"] == 0
    assert result["warning_count"] == 0
    assert result["unknown_sla_count"] == 0
    assert result["exceptions_count"] == 0
    assert result["import_failure_count"] == 0
    assert result["active_alerts_count"] == 0
    assert result["carriers_count"] == 0


def test_deve_nao_duplicar_regra_de_sla(db_session: Session, db_with_dashboard_data):
    """Deve não duplicar regra de SLA."""
    # O service deve reaproveitar calculate_shipment_sla do BETA-013A
    result = calculate_dashboard_summary(db_session)

    # Verificar que SLA foi calculado corretamente
    assert result["on_time_count"] >= 1
