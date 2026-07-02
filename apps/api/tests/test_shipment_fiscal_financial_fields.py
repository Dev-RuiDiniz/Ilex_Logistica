"""
Testes TDD para campos fiscais/financeiros de Shipment

Este arquivo contém testes para validar a implementação dos campos
fiscais/financeiros conforme BETA-011A.
"""

from datetime import UTC, datetime
from sqlalchemy.orm import Session

from app.modules.shipments.models import Shipment
from app.modules.shipments.schemas import ShipmentListItem, ShipmentDetailResponse


def test_shipment_with_fiscal_financial_fields(db_session: Session):
    """Deve criar entrega com valor da NF e valor do frete."""
    # Este teste falhará até que implementemos os campos
    shipment = Shipment(
        tracking_code="TEST123",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        # Campos fiscais/financeiros
        invoice_number="NF123456",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Verificar que os campos foram persistidos
    assert shipment.invoice_number == "NF123456"
    assert shipment.freight_value == 100.0
    assert shipment.invoice_value == 1000.0
    assert shipment.collection_departure_date is not None
    assert shipment.customer_name == "Test Customer"
    assert shipment.destination_uf == "SP"


def test_freight_percentage_calculation(db_session: Session):
    """Deve calcular percentual do frete corretamente."""
    shipment = Shipment(
        tracking_code="TEST456",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF789012",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # freight_percentage = freight_value / invoice_value * 100
    # 100.0 / 1000.0 * 100 = 10.0
    assert shipment.freight_percentage == 10.0


def test_freight_percentage_null_when_invoice_value_zero(db_session: Session):
    """Deve retornar percentual null quando valor da NF for zero."""
    shipment = Shipment(
        tracking_code="TEST789",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF345678",
        freight_value=100.0,
        invoice_value=0.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Deve ser null quando invoice_value é zero
    assert shipment.freight_percentage is None


def test_freight_percentage_null_when_invoice_value_null(db_session: Session):
    """Deve retornar percentual null quando valor da NF estiver ausente."""
    shipment = Shipment(
        tracking_code="TEST012",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF901234",
        freight_value=100.0,
        invoice_value=None,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Deve ser null quando invoice_value é None
    assert shipment.freight_percentage is None


def test_freight_percentage_null_when_freight_value_null(db_session: Session):
    """Deve retornar percentual null quando valor do frete estiver ausente."""
    shipment = Shipment(
        tracking_code="TEST345",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF567890",
        freight_value=None,
        invoice_value=1000.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Deve ser null quando freight_value é None
    assert shipment.freight_percentage is None


def test_collection_departure_date_persistence(db_session: Session):
    """Deve persistir data de coleta/saída."""
    collection_date = datetime(2026, 6, 8, 10, 0, 0, tzinfo=UTC)
    
    shipment = Shipment(
        tracking_code="TEST678",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF234567",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=collection_date,
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Verificar que a data foi persistida (comparação mais flexível)
    assert shipment.collection_departure_date is not None
    assert shipment.collection_departure_date.year == 2026
    assert shipment.collection_departure_date.month == 6
    assert shipment.collection_departure_date.day == 8


def test_fiscal_financial_fields_in_list_schema(db_session: Session):
    """Deve expor campos fiscais/financeiros na listagem."""
    shipment = Shipment(
        tracking_code="TEST901",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF890123",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Converter para schema de listagem
    item_data = {
        "id": shipment.id,
        "tracking_code": shipment.tracking_code,
        "carrier_id": shipment.carrier_id,
        "status": shipment.status,
        "estimated_delivery": shipment.estimated_delivery,
        "recipient_name": shipment.recipient_name,
        "recipient_phone": shipment.recipient_phone,
        "origin_address": shipment.origin_address,
        "destination_address": shipment.destination_address,
        "invoice_number": shipment.invoice_number,
        "invoice_key": shipment.invoice_key,
        "fiscal_document": shipment.fiscal_document,
        "amount": shipment.amount,
        "due_date": shipment.due_date,
        "delay_days": shipment.delay_days,
        "criticality": shipment.criticality,
        "freight_value": shipment.freight_value,
        "invoice_value": shipment.invoice_value,
        "freight_percentage": shipment.freight_percentage,
        "collection_departure_date": shipment.collection_departure_date,
        "customer_name": shipment.customer_name,
        "destination_uf": shipment.destination_uf,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
    }
    
    # Validar schema
    item = ShipmentListItem(**item_data)
    
    assert item.invoice_number == "NF890123"
    assert item.freight_value == 100.0
    assert item.invoice_value == 1000.0
    assert item.freight_percentage == 10.0
    assert item.collection_departure_date is not None
    assert item.customer_name == "Test Customer"
    assert item.destination_uf == "SP"


def test_fiscal_financial_fields_in_detail_schema(db_session: Session):
    """Deve expor campos fiscais/financeiros no detalhe."""
    shipment = Shipment(
        tracking_code="TEST234",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test Customer",
        recipient_phone="11999999999",
        origin_address="Rua Teste, 1",
        destination_address="Rua Destino, 1",
        invoice_number="NF456789",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=datetime.now(UTC),
        customer_name="Test Customer",
        destination_uf="SP",
    )
    
    db_session.add(shipment)
    db_session.commit()
    db_session.refresh(shipment)
    
    # Converter para schema de detalhe
    item_data = {
        "id": shipment.id,
        "tracking_code": shipment.tracking_code,
        "carrier_id": shipment.carrier_id,
        "status": shipment.status,
        "estimated_delivery": shipment.estimated_delivery,
        "recipient_name": shipment.recipient_name,
        "recipient_phone": shipment.recipient_phone,
        "origin_address": shipment.origin_address,
        "destination_address": shipment.destination_address,
        "invoice_number": shipment.invoice_number,
        "invoice_key": shipment.invoice_key,
        "fiscal_document": shipment.fiscal_document,
        "amount": shipment.amount,
        "due_date": shipment.due_date,
        "delay_days": shipment.delay_days,
        "criticality": shipment.criticality,
        "freight_value": shipment.freight_value,
        "invoice_value": shipment.invoice_value,
        "freight_percentage": shipment.freight_percentage,
        "collection_departure_date": shipment.collection_departure_date,
        "customer_name": shipment.customer_name,
        "destination_uf": shipment.destination_uf,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
    }
    
    # Validar schema (ShipmentDetailResponse herda de ShipmentListItem)
    item = ShipmentDetailResponse(**item_data)
    
    assert item.invoice_number == "NF456789"
    assert item.freight_value == 100.0
    assert item.invoice_value == 1000.0
    assert item.freight_percentage == 10.0
    assert item.collection_departure_date is not None
    assert item.customer_name == "Test Customer"
    assert item.destination_uf == "SP"


def test_backward_compatibility_with_old_shipments(db_session: Session):
    """Deve manter compatibilidade com entrega antiga sem esses campos."""
    # Criar shipment antigo sem os novos campos
    old_shipment = Shipment(
        tracking_code="OLD123",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Old Customer",
        recipient_phone="11999999999",
        origin_address="Rua Antiga, 1",
        destination_address="Rua Antiga Destino, 1",
    )
    
    db_session.add(old_shipment)
    db_session.commit()
    db_session.refresh(old_shipment)
    
    # Campos novos devem ser None
    assert old_shipment.freight_value is None
    assert old_shipment.invoice_value is None
    assert old_shipment.freight_percentage is None
    assert old_shipment.collection_departure_date is None
    assert old_shipment.customer_name is None
    assert old_shipment.destination_uf is None
