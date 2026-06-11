"""
Fixtures para dados sintéticos de homologação E2E beta.

Estes fixtures fornecem dados sintéticos para simular o fluxo completo:
importação → validação → persistência → cálculo → exceções → tratativas → alertas → relatório diário → auditoria → RBAC/frontend.
"""

import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.sla.models import SlaRule


@pytest.fixture
def synthetic_carriers(db_session: Session):
    """Cria transportadoras sintéticas para homologação."""
    carriers = [
        Carrier(name="Braspress"),
        Carrier(name="TranspSynth1"),
        Carrier(name="TranspSynth2"),
    ]
    for carrier in carriers:
        db_session.add(carrier)
    db_session.commit()
    return carriers


@pytest.fixture
def synthetic_sla_rules(db_session: Session, synthetic_carriers):
    """Cria regras SLA sintéticas para homologação."""
    braspress = synthetic_carriers[0]
    transp1 = synthetic_carriers[1]
    
    rules = [
        # Regra global (default)
        SlaRule(
            carrier_id=None,
            destination_uf=None,
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True
        ),
        # Regra específica para Braspress
        SlaRule(
            carrier_id=braspress.id,
            destination_uf=None,
            transit_days=7,
            warning_threshold_days=3,
            critical_delay_days=4,
            is_active=True
        ),
        # Regra específica para TranspSynth1 em SP
        SlaRule(
            carrier_id=transp1.id,
            destination_uf="SP",
            transit_days=3,
            warning_threshold_days=1,
            critical_delay_days=2,
            is_active=True
        ),
    ]
    for rule in rules:
        db_session.add(rule)
    db_session.commit()
    return rules


@pytest.fixture
def synthetic_exception_rules(db_session: Session):
    """Cria regras de exceção sintéticas para homologação."""
    # Nota: exceções são tratadas via SLA service, não há tabela de ExceptionRule
    # Este fixture é um placeholder para compatibilidade
    return []


@pytest.fixture
def synthetic_shipments(db_session: Session, synthetic_carriers):
    """Cria shipments sintéticos para homologação cobrindo todos os cenários."""
    braspress = synthetic_carriers[0]
    transp1 = synthetic_carriers[1]
    transp2 = synthetic_carriers[2]
    
    today = date.today()
    
    shipments = [
        # Shipment válido (no prazo)
        Shipment(
            tracking_code="SYNTH-001",
            carrier_id=braspress.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=5),
            actual_delivery=today - timedelta(days=4),
            recipient_name="Cliente Sintético 1",
            recipient_phone="11999999999",
            origin_address="Rua Origem 1, SP",
            destination_address="Rua Destino 1, SP",
            invoice_number="INV-001",
            invoice_value=1000.00,
            freight_value=50.00,
            customer_name="Cliente Sintético 1",
            destination_uf="SP"
        ),
        # Shipment com atraso (late)
        Shipment(
            tracking_code="SYNTH-002",
            carrier_id=transp1.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=3),
            actual_delivery=today,  # Entregue com atraso
            recipient_name="Cliente Sintético 2",
            recipient_phone="21999999999",
            origin_address="Rua Origem 2, RJ",
            destination_address="Rua Destino 2, RJ",
            invoice_number="INV-002",
            invoice_value=2000.00,
            freight_value=100.00,
            customer_name="Cliente Sintético 2",
            destination_uf="RJ"
        ),
        # Shipment com atraso crítico (critical)
        Shipment(
            tracking_code="SYNTH-003",
            carrier_id=transp2.id,
            status="delivered",
            estimated_delivery=today - timedelta(days=1),
            actual_delivery=today,  # Entregue com atraso crítico
            recipient_name="Cliente Sintético 3",
            recipient_phone="31999999999",
            origin_address="Rua Origem 3, MG",
            destination_address="Rua Destino 3, MG",
            invoice_number="INV-003",
            invoice_value=1500.00,
            freight_value=75.00,
            customer_name="Cliente Sintético 3",
            destination_uf="MG"
        ),
        # Shipment em trânsito (on time)
        Shipment(
            tracking_code="SYNTH-004",
            carrier_id=braspress.id,
            status="in_transit",
            estimated_delivery=today + timedelta(days=3),
            actual_delivery=None,
            recipient_name="Cliente Sintético 4",
            recipient_phone="51999999999",
            origin_address="Rua Origem 4, RS",
            destination_address="Rua Destino 4, RS",
            invoice_number="INV-004",
            invoice_value=800.00,
            freight_value=40.00,
            customer_name="Cliente Sintético 4",
            destination_uf="RS"
        ),
        # Shipment em trânsito (late)
        Shipment(
            tracking_code="SYNTH-005",
            carrier_id=transp1.id,
            status="in_transit",
            estimated_delivery=today - timedelta(days=1),
            actual_delivery=None,  # Ainda não entregue, já está late
            recipient_name="Cliente Sintético 5",
            recipient_phone="41999999999",
            origin_address="Rua Origem 5, PR",
            destination_address="Rua Destino 5, PR",
            invoice_number="INV-005",
            invoice_value=1200.00,
            freight_value=60.00,
            customer_name="Cliente Sintético 5",
            destination_uf="PR"
        ),
    ]
    
    for shipment in shipments:
        db_session.add(shipment)
    db_session.commit()
    
    return shipments


@pytest.fixture
def synthetic_braspress_csv_content():
    """Conteúdo CSV sintético para importação Braspress."""
    return """Tracking Code,Invoice Number,Customer Name,Destination UF,Collection Date,Invoice Value,Freight Value,Carrier
SYNTH-BRAS-001,INV-BRAS-001,Cliente Braspress 1,SP,01/01/2026,1000.00,50.00,Braspress
SYNTH-BRAS-002,INV-BRAS-002,Cliente Braspress 2,RJ,02/01/2026,2000.00,100.00,Braspress
SYNTH-BRAS-003,INV-BRAS-003,Cliente Braspress 3,MG,03/01/2026,1500.00,75.00,Braspress
"""
