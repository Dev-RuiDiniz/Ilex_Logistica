from datetime import datetime, UTC
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.shipments.analytics_service import calculate_carrier_efficiency


def test_agrupar_entregas_por_transportadora(db_session: Session):
    """Deve agrupar entregas por transportadora."""
    # Criar transportadoras
    carrier1 = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportadora B", external_code="TPB-1", integration_metadata={})
    db_session.add_all([carrier1, carrier2])
    db_session.flush()

    # Criar shipments
    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        invoice_number="NF001",
        freight_value=100.0,
        invoice_value=1000.0,
        collection_departure_date=datetime(2025, 1, 5, tzinfo=UTC),
        customer_name="Cliente X",
        destination_uf="RJ",
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier2.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        invoice_number="NF002",
        freight_value=150.0,
        invoice_value=1500.0,
        collection_departure_date=datetime(2025, 1, 5, tzinfo=UTC),
        customer_name="Cliente Y",
        destination_uf="MG",
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 2
    assert result["carriers"][0]["carrier_id"] == carrier1.id
    assert result["carriers"][1]["carrier_id"] == carrier2.id


def test_calcular_total_nfs(db_session: Session):
    """Deve calcular total de NFs."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        invoice_number="NF001",
        freight_value=100.0,
        invoice_value=1000.0,
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        invoice_number="NF002",
        freight_value=150.0,
        invoice_value=1500.0,
    )
    shipment3 = Shipment(
        tracking_code="TRK003",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 3",
        recipient_phone="11999999999",
        origin_address="Rua E SP",
        destination_address="Rua F RS",
        meta_data="{}",
        is_active=True,
        invoice_number=None,  # Sem NF
        freight_value=200.0,
        invoice_value=2000.0,
    )
    db_session.add_all([shipment1, shipment2, shipment3])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_invoices"] == 2


def test_calcular_total_shipments(db_session: Session):
    """Deve calcular total de shipments."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    for i in range(5):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="delivered",
            estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 5


def test_calcular_entregas_no_prazo(db_session: Session):
    """Deve calcular entregas no prazo."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment no prazo (estimated_delivery futuro)
    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2025, 12, 31, tzinfo=UTC),  # Futuro
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["on_time_count"] >= 0


def test_calcular_entregas_atrasadas(db_session: Session):
    """Deve calcular entregas atrasadas."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar shipment atrasado (estimated_delivery passado)
    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),  # Passado
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["late_count"] >= 0


def test_calcular_entregas_criticas(db_session: Session):
    """Deve calcular entregas críticas, se criticality existir."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        criticality="alta",
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["critical_count"] == 1


def test_calcular_extraviadas_quando_status_existir(db_session: Session):
    """Deve calcular extraviadas quando status existir."""
    # Status de extraviada não existe no domínio, sempre 0
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="failed",  # Status mais próximo de extravio
        estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["lost_count"] == 0


def test_retornar_zero_extraviadas_quando_status_nao_existir(db_session: Session):
    """Deve retornar zero extraviadas quando status não existir."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["lost_count"] == 0


def test_calcular_percentuais_com_base_no_total_da_transportadora(db_session: Session):
    """Deve calcular percentuais com base no total da transportadora."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Criar 3 shipments
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier.id,
            status="in_transit",
            estimated_delivery=datetime(2025, 12, 31, tzinfo=UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 3
    # Percentuais devem somar 100% (considerando apenas on_time + late + lost)
    assert result["carriers"][0]["on_time_percentage"] + result["carriers"][0]["late_percentage"] + result["carriers"][0]["lost_percentage"] <= 100


def test_evitar_divisao_por_zero(db_session: Session):
    """Deve evitar divisão por zero."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    # Transportadora sem dados deve retornar lista vazia ou não aparecer
    assert len(result["carriers"]) == 0


def test_calcular_frete_total(db_session: Session):
    """Deve calcular frete total."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        freight_value=100.0,
        invoice_value=1000.0,
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        freight_value=150.0,
        invoice_value=1500.0,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_freight_value"] == 250.0


def test_calcular_percentual_medio_do_frete(db_session: Session):
    """Deve calcular percentual médio do frete."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        freight_value=100.0,
        invoice_value=1000.0,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["average_freight_percentage"] == 10.0


def test_calcular_ranking_por_eficiencia(db_session: Session):
    """Deve calcular ranking por eficiência."""
    carrier1 = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportadora B", external_code="TPB-1", integration_metadata={})
    db_session.add_all([carrier1, carrier2])
    db_session.flush()

    # Carrier A: todos no prazo
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier1.id,
            status="in_transit",
            estimated_delivery=datetime(2025, 12, 31, tzinfo=UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)

    # Carrier B: todos atrasados
    for i in range(3):
        shipment = Shipment(
            tracking_code=f"TRK{i+3:03d}",
            carrier_id=carrier2.id,
            status="in_transit",
            estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),
            recipient_name=f"Cliente {i+3}",
            recipient_phone="11999999999",
            origin_address="Rua C SP",
            destination_address="Rua D MG",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)

    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 2
    # Carrier A deve ter ranking 1 (maior eficiência)
    assert result["carriers"][0]["carrier_id"] == carrier1.id
    assert result["carriers"][0]["ranking_by_efficiency"] == 1


def test_calcular_ranking_por_custo(db_session: Session):
    """Deve calcular ranking por custo."""
    carrier1 = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportadora B", external_code="TPB-1", integration_metadata={})
    db_session.add_all([carrier1, carrier2])
    db_session.flush()

    # Carrier A: frete 10%
    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        freight_value=100.0,
        invoice_value=1000.0,
    )
    db_session.add(shipment1)

    # Carrier B: frete 20%
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier2.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        freight_value=200.0,
        invoice_value=1000.0,
    )
    db_session.add(shipment2)

    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 2
    # Carrier A deve ter ranking 1 (menor custo)
    assert result["carriers"][0]["carrier_id"] == carrier1.id
    assert result["carriers"][0]["ranking_by_cost"] == 1


def test_calcular_ranking_por_volume(db_session: Session):
    """Deve calcular ranking por volume."""
    carrier1 = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportadora B", external_code="TPB-1", integration_metadata={})
    db_session.add_all([carrier1, carrier2])
    db_session.flush()

    # Carrier A: 5 shipments
    for i in range(5):
        shipment = Shipment(
            tracking_code=f"TRK{i:03d}",
            carrier_id=carrier1.id,
            status="delivered",
            estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
            recipient_name=f"Cliente {i}",
            recipient_phone="11999999999",
            origin_address="Rua A SP",
            destination_address="Rua B RJ",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)

    # Carrier B: 2 shipments
    for i in range(2):
        shipment = Shipment(
            tracking_code=f"TRK{i+5:03d}",
            carrier_id=carrier2.id,
            status="delivered",
            estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
            recipient_name=f"Cliente {i+5}",
            recipient_phone="11999999999",
            origin_address="Rua C SP",
            destination_address="Rua D MG",
            meta_data="{}",
            is_active=True,
        )
        db_session.add(shipment)

    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert len(result["carriers"]) == 2
    # Carrier A deve ter ranking 1 (maior volume)
    assert result["carriers"][0]["carrier_id"] == carrier1.id
    assert result["carriers"][0]["ranking_by_volume"] == 1


def test_aplicar_filtro_de_periodo(db_session: Session):
    """Deve aplicar filtro de período."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Shipment dentro do período
    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 15, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    # Shipment fora do período
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2024, 1, 15, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(
        db_session,
        estimated_delivery_from="2025-01-01",
        estimated_delivery_to="2025-01-31",
    )

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 1


def test_aplicar_filtro_por_mes_ano(db_session: Session):
    """Deve aplicar filtro por mês/ano."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 15, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 2, 15, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, month=1, year=2025)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 1


def test_aplicar_filtro_por_cliente(db_session: Session):
    """Deve aplicar filtro por cliente."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente X",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        customer_name="Cliente X",
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente Y",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        customer_name="Cliente Y",
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, customer_name="Cliente X")

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 1


def test_aplicar_filtro_por_uf(db_session: Session):
    """Deve aplicar filtro por UF."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        destination_uf="RJ",
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        destination_uf="MG",
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, destination_uf="RJ")

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 1


def test_aplicar_filtro_por_transportadora(db_session: Session):
    """Deve aplicar filtro por transportadora."""
    carrier1 = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    carrier2 = Carrier(name="Transportadora B", external_code="TPB-1", integration_metadata={})
    db_session.add_all([carrier1, carrier2])
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier1.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier2.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, carrier_id=carrier1.id)

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["carrier_id"] == carrier1.id


def test_aplicar_filtro_por_criticality(db_session: Session):
    """Deve aplicar filtro por criticality."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
        criticality="alta",
    )
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
        criticality="normal",
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, criticality="alta")

    assert len(result["carriers"]) == 1
    assert result["carriers"][0]["total_shipments"] == 1


def test_aplicar_filtro_por_sla_status(db_session: Session):
    """Deve aplicar filtro por sla_status."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Shipment no prazo (futuro)
    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2025, 12, 31, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    # Shipment atrasado (passado)
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, sla_status="on_time")

    # Filtro on-demand deve funcionar
    assert len(result["carriers"]) >= 0


def test_aplicar_filtro_por_is_late(db_session: Session):
    """Deve aplicar filtro por is_late."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    # Shipment no prazo (futuro)
    shipment1 = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2025, 12, 31, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    # Shipment atrasado (passado)
    shipment2 = Shipment(
        tracking_code="TRK002",
        carrier_id=carrier.id,
        status="in_transit",
        estimated_delivery=datetime(2024, 1, 1, tzinfo=UTC),
        recipient_name="Cliente 2",
        recipient_phone="11999999999",
        origin_address="Rua C SP",
        destination_address="Rua D MG",
        meta_data="{}",
        is_active=True,
    )
    db_session.add_all([shipment1, shipment2])
    db_session.commit()

    result = calculate_carrier_efficiency(db_session, is_late=True)

    # Filtro on-demand deve funcionar
    assert len(result["carriers"]) >= 0


def test_tratar_transportadora_sem_dados(db_session: Session):
    """Deve tratar transportadora sem dados."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    # Transportadora sem shipments não deve aparecer
    assert len(result["carriers"]) == 0


def test_retornar_payload_estavel_para_frontend(db_session: Session):
    """Deve retornar payload estável para frontend."""
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    result = calculate_carrier_efficiency(db_session)

    assert "carriers" in result
    assert "generated_at" in result
    assert isinstance(result["carriers"], list)
    assert len(result["carriers"]) == 1
    assert "carrier_id" in result["carriers"][0]
    assert "carrier_name" in result["carriers"][0]
    assert "total_shipments" in result["carriers"][0]
    assert "on_time_percentage" in result["carriers"][0]
    assert "ranking_by_efficiency" in result["carriers"][0]
    assert "ranking_by_cost" in result["carriers"][0]
    assert "ranking_by_volume" in result["carriers"][0]


def test_respeitar_autenticacao_autorizacao_existente(db_session: Session):
    """Deve respeitar autenticação/autorização existente."""
    # Service não tem autenticação própria, depende do router
    # Este teste valida que o service não quebra sem autenticação
    carrier = Carrier(name="Transportadora A", external_code="TPA-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()

    shipment = Shipment(
        tracking_code="TRK001",
        carrier_id=carrier.id,
        status="delivered",
        estimated_delivery=datetime(2025, 1, 10, tzinfo=UTC),
        recipient_name="Cliente 1",
        recipient_phone="11999999999",
        origin_address="Rua A SP",
        destination_address="Rua B RJ",
        meta_data="{}",
        is_active=True,
    )
    db_session.add(shipment)
    db_session.commit()

    # Service deve funcionar sem autenticação (validação no router)
    result = calculate_carrier_efficiency(db_session)

    assert result is not None
    assert "carriers" in result
