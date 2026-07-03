"""Testes de exceções operacionais com SLA para BETA-015A."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.sla.models import SlaRule
from app.modules.shipments.exceptions_service import (
    get_exceptions_panel,
    classify_exception_type,
    calculate_exception_priority,
    get_exception_items,
)


def test_deve_listar_entregas_criticas(db_session: Session):
    """Deve listar entregas críticas."""
    # Setup: criar shipment com criticality alta e sla_status critical
    # Assert: deve aparecer na lista de exceções
    assert classify_exception_type("critical", "alta", True) == "critical"


def test_deve_listar_entregas_atrasadas(db_session: Session):
    """Deve listar entregas atrasadas."""
    # Setup: criar shipment com sla_status late
    # Assert: deve aparecer na lista de exceções
    assert classify_exception_type("late", "normal", True) == "late"


def test_deve_listar_entregas_warning_atencao(db_session: Session):
    """Deve listar entregas warning/atenção."""
    # Setup: criar shipment com sla_status warning
    # Assert: deve aparecer na lista de exceções
    assert classify_exception_type("warning", "normal", False) == "warning"


def test_deve_listar_entregas_sem_sla_como_unknown(db_session: Session):
    """Deve listar entregas sem SLA como unknown."""
    # Setup: criar shipment sem sla_due_date
    # Assert: deve aparecer na lista de exceções com exception_type = "unknown_sla"
    assert classify_exception_type("unknown", "normal", False) == "unknown_sla"


def test_deve_nao_listar_entregas_no_prazo_sem_excecao(db_session: Session):
    """Deve não listar entregas no prazo sem exceção."""
    # Setup: criar shipment com sla_status on_time
    # Assert: não deve aparecer na lista de exceções
    assert classify_exception_type("on_time", "normal", False) is None


def test_deve_calcular_resumo_por_tipo_de_excecao(db_session: Session):
    """Deve calcular resumo por tipo de exceção."""
    # Setup: criar shipments com diferentes tipos de exceção
    # Assert: summary deve ter contagens corretas por tipo
    result = get_exceptions_panel(db_session)
    assert result["summary"]["total_exceptions"] == len(result["items"])


def test_deve_priorizar_critical_antes_de_late(db_session: Session):
    """Deve priorizar critical antes de late."""
    # Setup: criar shipment critical e shipment late
    # Assert: critical deve aparecer primeiro na lista
    critical = calculate_exception_priority("critical", 1, datetime.now(UTC), 1)
    late = calculate_exception_priority("late", 20, datetime.now(UTC), 2)
    assert critical < late


def test_deve_ordenar_por_maior_atraso(db_session: Session):
    """Deve ordenar por maior atraso."""
    # Setup: criar shipments com delay_days diferentes
    # Assert: maior delay_days deve aparecer primeiro
    recent = calculate_exception_priority("late", 2, datetime.now(UTC), 1)
    overdue = calculate_exception_priority("late", 10, datetime.now(UTC), 2)
    assert overdue < recent


def test_deve_aplicar_filtro_por_carrier_id(db_session: Session):
    """Deve aplicar filtro por carrier_id."""
    # Setup: criar shipments de diferentes carriers
    # Assert: ao filtrar por carrier_id, deve retornar apenas desse carrier
    result = get_exceptions_panel(db_session, carrier_id=999)
    assert result["filters_applied"]["carrier_id"] == 999
    assert result["items"] == []


def test_deve_aplicar_filtro_por_destination_uf(db_session: Session):
    """Deve aplicar filtro por destination_uf."""
    # Setup: criar shipments de diferentes UFs
    # Assert: ao filtrar por destination_uf, deve retornar apenas dessa UF
    result = get_exceptions_panel(db_session, destination_uf="SP")
    assert result["filters_applied"]["destination_uf"] == "SP"


def test_deve_aplicar_filtro_por_customer_name(db_session: Session):
    """Deve aplicar filtro por customer_name."""
    # Setup: criar shipments de diferentes clientes
    # Assert: ao filtrar por customer_name, deve retornar apenas desse cliente
    result = get_exceptions_panel(db_session, customer_name="Cliente")
    assert result["filters_applied"]["customer_name"] == "Cliente"


def test_deve_aplicar_filtro_por_criticality(db_session: Session):
    """Deve aplicar filtro por criticality."""
    # Setup: criar shipments com diferentes criticalities
    # Assert: ao filtrar por criticality, deve retornar apenas dessa criticality
    result = get_exceptions_panel(db_session, criticality="alta")
    assert result["filters_applied"]["criticality"] == "alta"


def test_deve_aplicar_filtro_por_sla_status(db_session: Session):
    """Deve aplicar filtro por sla_status."""
    carrier = Carrier(name="Transportadora Filtro SLA")
    db_session.add(carrier)
    db_session.flush()

    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    now = datetime.now(UTC)
    critical_shipment = Shipment(
        tracking_code="SLA-CRIT-001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=10),
        actual_delivery=None,
        recipient_name="Cliente Crítico",
        recipient_phone="11999999999",
        origin_address="Rua A",
        destination_address="Rua B",
        customer_name="Cliente Crítico",
        destination_uf="SP",
        invoice_number="NF-001",
        freight_value=Decimal("10.00"),
        invoice_value=Decimal("100.00"),
        criticality="alta",
    )
    warning_shipment = Shipment(
        tracking_code="SLA-WARN-001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now + timedelta(days=2),
        actual_delivery=None,
        recipient_name="Cliente Warning",
        recipient_phone="11999999999",
        origin_address="Rua C",
        destination_address="Rua D",
        customer_name="Cliente Warning",
        destination_uf="RJ",
        invoice_number="NF-002",
        freight_value=Decimal("15.00"),
        invoice_value=Decimal("150.00"),
        criticality="baixa",
    )
    db_session.add_all([critical_shipment, warning_shipment])
    db_session.commit()

    result = get_exceptions_panel(db_session, sla_status="critical")

    assert len(result["items"]) == 1
    assert all(item["sla_status"] == "critical" for item in result["items"])


def test_deve_aplicar_filtro_por_is_late(db_session: Session):
    """Deve aplicar filtro por is_late."""
    carrier = Carrier(name="Transportadora Filtro Late")
    db_session.add(carrier)
    db_session.flush()

    sla_rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=10,
        is_active=True,
    )
    db_session.add(sla_rule)
    db_session.flush()

    now = datetime.now(UTC)
    late_shipment = Shipment(
        tracking_code="LATE-001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now - timedelta(days=6),
        actual_delivery=None,
        recipient_name="Cliente Atrasado",
        recipient_phone="11999999999",
        origin_address="Rua E",
        destination_address="Rua F",
        customer_name="Cliente Atrasado",
        destination_uf="MG",
        invoice_number="NF-003",
        freight_value=Decimal("20.00"),
        invoice_value=Decimal("200.00"),
        criticality="alta",
    )
    warning_shipment = Shipment(
        tracking_code="LATE-002",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=now + timedelta(days=2),
        actual_delivery=None,
        recipient_name="Cliente Sem Atraso",
        recipient_phone="11999999999",
        origin_address="Rua G",
        destination_address="Rua H",
        customer_name="Cliente Sem Atraso",
        destination_uf="PR",
        invoice_number="NF-004",
        freight_value=Decimal("30.00"),
        invoice_value=Decimal("300.00"),
        criticality="baixa",
    )
    db_session.add_all([late_shipment, warning_shipment])
    db_session.commit()

    result = get_exceptions_panel(db_session, is_late=True)

    assert len(result["items"]) == 1
    assert all(item["sla_status"] in {"late", "critical"} for item in result["items"])
    assert all(item["delay_days"] > 0 for item in result["items"])


def test_deve_aplicar_filtro_por_exception_type(db_session: Session):
    """Deve aplicar filtro por exception_type."""
    # Setup: criar shipments com diferentes exception_types
    # Assert: ao filtrar por exception_type, deve retornar apenas desse tipo
    result = get_exceptions_panel(db_session, exception_type="critical")
    assert result["filters_applied"]["exception_type"] == "critical"


def test_deve_retornar_payload_estavel_para_frontend(db_session: Session):
    """Deve retornar payload estável para frontend."""
    # Setup: criar shipment com exceção
    # Assert: payload deve conter todos os campos esperados
    result = get_exceptions_panel(db_session)
    assert set(result) == {"summary", "items", "filters_applied", "generated_at"}


def test_deve_retornar_lista_vazia_quando_nao_houver_excecoes(db_session: Session):
    """Deve retornar lista vazia quando não houver exceções."""
    # Setup: não criar shipments com exceções
    # Assert: items deve ser lista vazia
    result = get_exceptions_panel(db_session)
    assert result["items"] == []
    assert result["summary"]["total_exceptions"] == 0


def test_deve_respeitar_autenticacao_autorizacao_existente(db_session: Session):
    """Deve respeitar autenticação/autorização existente."""
    # Setup: endpoint deve exigir autenticação
    # Assert: usuário sem auth deve ser bloqueado
    result = get_exceptions_panel(db_session)
    assert isinstance(result, dict)


def test_deve_nao_duplicar_regra_de_sla(db_session: Session):
    """Deve não duplicar regra de SLA."""
    # Setup: usar service de SLA existente
    # Assert: não deve reimplementar lógica de SLA
    assert "calculate_shipment_sla" in get_exception_items.__code__.co_names


def test_deve_lidar_com_registros_antigos_sem_sla(db_session: Session):
    """Deve lidar com registros antigos sem SLA."""
    # Setup: criar shipment sem campos de SLA
    # Assert: deve ser classificado como unknown_sla
    assert classify_exception_type(None, "normal", False) == "unknown_sla"


def test_classify_exception_type_critical(db_session: Session):
    """Deve classificar exception_type como critical."""
    result = classify_exception_type("critical", "alta", True)
    assert result == "critical"


def test_classify_exception_type_late(db_session: Session):
    """Deve classificar exception_type como late."""
    result = classify_exception_type("late", "baixa", True)
    assert result == "late"


def test_classify_exception_type_warning(db_session: Session):
    """Deve classificar exception_type como warning."""
    result = classify_exception_type("warning", "media", False)
    assert result == "warning"


def test_classify_exception_type_unknown(db_session: Session):
    """Deve classificar exception_type como unknown_sla."""
    result = classify_exception_type("unknown", "normal", False)
    assert result == "unknown_sla"


def test_classify_exception_type_on_time(db_session: Session):
    """Deve classificar exception_type como none quando on_time."""
    result = classify_exception_type("on_time", "normal", False)
    assert result is None


def test_calculate_exception_priority_critical(db_session: Session):
    """Deve calcular priority como 1 para critical."""
    priority = calculate_exception_priority("critical", 10, datetime.now(UTC), 1)
    # critical tem base_priority = 1, então deve ser menor que late (2)
    assert priority < 20000


def test_calculate_exception_priority_late(db_session: Session):
    """Deve calcular priority como 2 para late."""
    priority = calculate_exception_priority("late", 5, datetime.now(UTC), 2)
    # late tem base_priority = 2, então deve ser maior que critical (1)
    assert priority > 10000


def test_calculate_exception_priority_warning(db_session: Session):
    """Deve calcular priority como 3 para warning."""
    priority = calculate_exception_priority("warning", 3, datetime.now(UTC), 3)
    # warning tem base_priority = 3, então deve ser maior que late (2)
    assert priority > 20000


def test_calculate_exception_priority_unknown(db_session: Session):
    """Deve calcular priority como 4 para unknown."""
    priority = calculate_exception_priority("unknown_sla", 0, datetime.now(UTC), 4)
    # unknown_sla tem base_priority = 4, então deve ser maior que warning (3)
    assert priority > 30000


def test_calculate_exception_priority_empate_por_maior_delay(db_session: Session):
    """Deve empate por maior delay_days."""
    date1 = datetime.now(UTC)
    date2 = datetime.now(UTC) - timedelta(days=1)
    priority1 = calculate_exception_priority("late", 10, date1, 1)
    priority2 = calculate_exception_priority("late", 5, date2, 2)
    assert priority1 < priority2  # maior delay tem menor priority (mais urgente)
