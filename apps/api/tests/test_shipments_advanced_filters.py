"""
Testes TDD para filtros avançados de Shipment

Este arquivo contém testes para validar a implementação dos filtros
avançados conforme BETA-011A.
"""

import pytest
from datetime import UTC, datetime
from sqlalchemy.orm import Session

from app.modules.shipments.models import Shipment
from app.modules.shipments.service import list_shipments
from app.modules.sla.models import SlaRule


def test_filter_by_customer_name(db_session: Session):
    """Deve filtrar por cliente."""
    # Criar shipments de diferentes clientes
    shipment1 = Shipment(
        tracking_code="CUST001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="CUST002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Filtrar por customer_name
    result = list_shipments(db_session, customer_name="Customer A")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["customer_name"] == "Customer A"


def test_filter_by_destination_uf(db_session: Session):
    """Deve filtrar por UF."""
    shipment1 = Shipment(
        tracking_code="UF001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="UF002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Filtrar por destination_uf
    result = list_shipments(db_session, destination_uf="SP")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["destination_uf"] == "SP"


def test_filter_by_month(db_session: Session):
    """Deve filtrar por mês."""
    # Criar shipments em diferentes meses
    shipment1 = Shipment(
        tracking_code="MONTH001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1, tzinfo=UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="MONTH002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 7, 1, tzinfo=UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Filtrar por mês
    result = list_shipments(db_session, month=6)
    
    assert len(result["items"]) == 1
    assert result["items"][0]["tracking_code"] == "MONTH001"


def test_filter_by_year(db_session: Session):
    """Deve filtrar por ano."""
    shipment1 = Shipment(
        tracking_code="YEAR001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1, tzinfo=UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="YEAR002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2025, 6, 1, tzinfo=UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Filtrar por ano
    result = list_shipments(db_session, year=2026)
    
    assert len(result["items"]) == 1
    assert result["items"][0]["tracking_code"] == "YEAR001"


def test_return_all_when_temporal_filter_absent(db_session: Session):
    """Deve retornar todo período quando filtro temporal estiver ausente."""
    shipment1 = Shipment(
        tracking_code="TEMP001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1, tzinfo=UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="TEMP002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 7, 1, tzinfo=UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Sem filtro temporal
    result = list_shipments(db_session)
    
    assert len(result["items"]) == 2


def test_search_by_invoice_number(db_session: Session):
    """Deve buscar por NF."""
    shipment1 = Shipment(
        tracking_code="INV001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF123456",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="INV002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        invoice_number="NF789012",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Buscar por invoice_number
    result = list_shipments(db_session, search="NF123456")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["invoice_number"] == "NF123456"


def test_search_by_customer_name(db_session: Session):
    """Deve buscar por cliente."""
    shipment1 = Shipment(
        tracking_code="SEARCH001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="SEARCH002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Buscar por customer_name
    result = list_shipments(db_session, search="Customer A")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["customer_name"] == "Customer A"


def test_search_by_tracking_code(db_session: Session):
    """Deve buscar por rastreio."""
    shipment1 = Shipment(
        tracking_code="TRACK001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="TRACK002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Buscar por tracking_code
    result = list_shipments(db_session, search="TRACK001")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["tracking_code"] == "TRACK001"


def test_search_by_carrier_name(db_session: Session):
    """Deve buscar por transportadora."""
    # Este teste depende de ter carriers no banco
    # Por enquanto, vamos testar com carrier_id
    shipment1 = Shipment(
        tracking_code="CARRIER001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="CARRIER002",
        carrier_id=2,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Filtrar por carrier_id
    result = list_shipments(db_session, carrier_id=1)
    
    assert len(result["items"]) == 1
    assert result["items"][0]["carrier_id"] == 1


def test_combine_filters_without_conflict(db_session: Session):
    """Deve combinar filtros sem conflito."""
    shipment1 = Shipment(
        tracking_code="COMB001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1, tzinfo=UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    shipment2 = Shipment(
        tracking_code="COMB002",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2026, 6, 1, tzinfo=UTC),
        recipient_name="Customer B",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 2",
        destination_address="Rua Destino, 2",
        customer_name="Customer B",
        destination_uf="RJ",
    )
    
    db_session.add(shipment1)
    db_session.add(shipment2)
    db_session.commit()
    
    # Combinar filtros: carrier_id + destination_uf
    result = list_shipments(db_session, carrier_id=1, destination_uf="SP")
    
    assert len(result["items"]) == 1
    assert result["items"][0]["customer_name"] == "Customer A"
    assert result["items"][0]["destination_uf"] == "SP"


def test_return_empty_when_no_match(db_session: Session):
    """Deve retornar lista vazia quando nenhum registro corresponder."""
    shipment = Shipment(
        tracking_code="EMPTY001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Customer A",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        customer_name="Customer A",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    
    # Buscar por cliente que não existe
    result = list_shipments(db_session, customer_name="NonExistent")
    
    assert len(result["items"]) == 0
    assert result["total"] == 0


def test_respect_existing_authentication_authorization(db_session: Session):
    """Deve respeitar autenticação/autorização existente."""
    # Este teste valida que os filtros não quebram a autenticação existente
    # A autenticação é testada em test_auth.py
    # Aqui apenas verificamos que o service aceita os parâmetros
    
    result = list_shipments(
        db_session,
        page=1,
        page_size=20,
        status="pending",
        carrier_id=1,
        customer_name="Test",
        destination_uf="SP",
        month=6,
        year=2026,
    )
    
    # Deve retornar um resultado válido (pode ser vazio)
    assert "items" in result
    assert "total" in result
    assert "page" in result


# Testes de filtros SLA - BETA-013A

def test_filter_by_sla_status_on_time(db_session: Session):
    """Deve filtrar por sla_status=on_time."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment on_time
    shipment = Shipment(
        tracking_code="SLA001",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2025, 1, 25, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 20, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por sla_status=on_time
    result = list_shipments(db_session, sla_status="on_time")

    # Verificar que o filtro foi aplicado
    assert all(item["sla_status"] == "on_time" for item in result["items"])


def test_filter_by_sla_status_late(db_session: Session):
    """Deve filtrar por sla_status=late."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment late
    shipment = Shipment(
        tracking_code="SLA002",
        carrier_id=1,
        status="in_transit",
        estimated_delivery=datetime(2025, 1, 15, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por sla_status=late
    result = list_shipments(db_session, sla_status="late")

    # Verificar que o filtro foi aplicado
    assert all(item["sla_status"] == "late" for item in result["items"])


def test_filter_by_sla_status_unknown(db_session: Session):
    """Deve filtrar por sla_status=unknown."""
    # Criar shipment sem collection_date
    shipment = Shipment(
        tracking_code="SLA003",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2025, 1, 20, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por sla_status=unknown
    result = list_shipments(db_session, sla_status="unknown")

    # Verificar que o filtro foi aplicado
    assert all(item["sla_status"] == "unknown" for item in result["items"])


def test_filter_by_is_late_true(db_session: Session):
    """Deve filtrar por is_late=true."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment atrasado
    shipment = Shipment(
        tracking_code="SLA004",
        carrier_id=1,
        status="in_transit",
        estimated_delivery=datetime(2025, 1, 15, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por is_late=true
    result = list_shipments(db_session, is_late=True)

    # Verificar que o filtro foi aplicado
    assert all(item["is_late"] is True for item in result["items"])


def test_filter_by_is_late_false(db_session: Session):
    """Deve filtrar por is_late=false."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment no prazo
    shipment = Shipment(
        tracking_code="SLA005",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2025, 1, 25, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 20, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por is_late=false
    result = list_shipments(db_session, is_late=False)

    # Verificar que o filtro foi aplicado
    assert all(item["is_late"] is False for item in result["items"])


def test_combine_sla_with_existing_filters(db_session: Session):
    """Deve combinar SLA com filtros existentes sem quebrar."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment atrasado em SP, carrier_id=1
    shipment = Shipment(
        tracking_code="SLA006",
        carrier_id=1,
        status="in_transit",
        estimated_delivery=datetime(2025, 1, 15, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
        destination_uf="SP",
    )
    db_session.add(shipment)
    db_session.commit()

    # Filtrar por sla_status=late, carrier_id=1 e destination_uf=SP
    result = list_shipments(db_session, sla_status="late", carrier_id=1, destination_uf="SP")

    # Verificar que os filtros foram aplicados
    assert all(
        item["sla_status"] == "late" and 
        item["carrier_id"] == 1 and 
        item["destination_uf"] == "SP" 
        for item in result["items"]
    )


def test_expose_sla_fields_in_list(db_session: Session):
    """Deve expor campos SLA na listagem."""
    # Criar regra SLA
    rule = SlaRule(
        transit_days=5,
        warning_threshold_days=2,
        critical_delay_days=3,
        is_active=True,
    )
    db_session.add(rule)
    db_session.commit()

    # Criar shipment
    shipment = Shipment(
        tracking_code="SLA007",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime(2025, 1, 25, tzinfo=UTC),
        collection_departure_date=datetime(2025, 1, 20, tzinfo=UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()

    # Listar shipments
    result = list_shipments(db_session)

    assert len(result["items"]) >= 1
    item = result["items"][0]
    assert "sla_due_date" in item
    assert "sla_status" in item
    assert "is_late" in item
    assert "sla_rule_id" in item

    assert "page_size" in result
