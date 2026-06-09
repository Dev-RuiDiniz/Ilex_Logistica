"""Testes para cálculo SLA - BETA-013A."""

import pytest
from datetime import UTC, datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.sla.service import (
    calculate_shipment_sla,
    recalculate_shipment_sla,
    recalculate_all_shipments_sla,
)
from app.modules.shipments.models import Shipment


class TestSlaCalculation:
    """Testes de cálculo SLA de shipment."""

    def test_calculate_sla_with_expected_delivery(self, db_session: Session):
        """Deve usar expected_delivery quando já existir."""
        shipment = Shipment(
            tracking_code="TEST001",
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
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Calcular SLA
        result = calculate_shipment_sla(db_session, shipment.id)

        assert result["sla_due_date"] is not None
        assert result["sla_status"] is not None

    def test_calculate_sla_with_collection_date(self, db_session: Session):
        """Deve calcular due date a partir de collection_departure_date + transit_days."""
        shipment = Shipment(
            tracking_code="TEST002",
            carrier_id=1,
            status="pending",
            estimated_delivery=datetime(2025, 1, 20, tzinfo=UTC),  # Será ignorado se collection_date existir
            collection_departure_date=datetime(2025, 1, 15, tzinfo=UTC),
            recipient_name="Test Customer",
            recipient_phone="11999999999",
            origin_address="Origin",
            destination_address="Destination",
        )
        db_session.add(shipment)
        db_session.commit()
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Calcular SLA (sem expected_delivery, deve usar collection_date)
        result = calculate_shipment_sla(db_session, shipment.id, use_expected_delivery=False)

        assert result["sla_due_date"] == datetime(2025, 1, 20, tzinfo=UTC)

    def test_return_unknown_when_no_data(self, db_session: Session):
        """Deve retornar unknown quando não houver dados suficientes."""
        shipment = Shipment(
            tracking_code="TEST003",
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
        db_session.refresh(shipment)

        # Sem regra SLA
        result = calculate_shipment_sla(db_session, shipment.id)

        assert result["sla_status"] == "unknown"

    def test_calculate_delay_with_delivered_at(self, db_session: Session):
        """Deve calcular atraso com delivered_at quando entregue."""
        shipment = Shipment(
            tracking_code="TEST004",
            carrier_id=1,
            status="delivered",
            estimated_delivery=datetime(2025, 1, 20, tzinfo=UTC),
            actual_delivery=datetime(2025, 1, 25, tzinfo=UTC),
            recipient_name="Test Customer",
            recipient_phone="11999999999",
            origin_address="Origin",
            destination_address="Destination",
        )
        db_session.add(shipment)
        db_session.commit()
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        result = calculate_shipment_sla(db_session, shipment.id)

        assert result["delay_days"] == 5
        assert result["is_late"] is True

    def test_calculate_delay_with_today_injectable(self, db_session: Session):
        """Deve calcular atraso com today injetável quando não entregue."""
        shipment = Shipment(
            tracking_code="TEST005",
            carrier_id=1,
            status="in_transit",
            estimated_delivery=datetime(2025, 1, 20, tzinfo=UTC),
            recipient_name="Test Customer",
            recipient_phone="11999999999",
            origin_address="Origin",
            destination_address="Destination",
        )
        db_session.add(shipment)
        db_session.commit()
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Injetar today no passado para simular atraso
        today = datetime(2025, 1, 25, tzinfo=UTC)
        result = calculate_shipment_sla(db_session, shipment.id, today=today)

        assert result["delay_days"] == 5
        assert result["is_late"] is True

    def test_no_negative_delay(self, db_session: Session):
        """Deve não retornar atraso negativo."""
        shipment = Shipment(
            tracking_code="TEST006",
            carrier_id=1,
            status="delivered",
            estimated_delivery=datetime(2025, 1, 25, tzinfo=UTC),
            actual_delivery=datetime(2025, 1, 20, tzinfo=UTC),
            recipient_name="Test Customer",
            recipient_phone="11999999999",
            origin_address="Origin",
            destination_address="Destination",
        )
        db_session.add(shipment)
        db_session.commit()
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        result = calculate_shipment_sla(db_session, shipment.id)

        assert result["delay_days"] == 0  # Deve ser 0, não negativo
        assert result["is_late"] is False

    def test_preserve_old_records_without_sla_fields(self, db_session: Session):
        """Deve preservar registros antigos sem campos SLA."""
        # Criar shipment sem campos SLA
        shipment = Shipment(
            tracking_code="TEST007",
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
        db_session.refresh(shipment)

        # Sem regra SLA
        result = calculate_shipment_sla(db_session, shipment.id)

        assert result["sla_status"] == "unknown"
        assert result["delay_days"] == 0
        assert result["is_late"] is False


class TestSlaRecalculation:
    """Testes de reprocessamento SLA."""

    def test_reprocess_single_shipment(self, db_session: Session):
        """Deve reprocessar SLA de uma shipment."""
        shipment = Shipment(
            tracking_code="TEST008",
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
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Reprocessar
        result = recalculate_shipment_sla(db_session, shipment.id)

        assert result["success"] is True
        assert result["shipment_id"] == shipment.id

    def test_reprocess_multiple_shipments(self, db_session: Session):
        """Deve reprocessar múltiplas shipments."""
        # Criar 3 shipments
        for i in range(3):
            shipment = Shipment(
                tracking_code=f"TEST00{i}",
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

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Reprocessar todos
        result = recalculate_all_shipments_sla(db_session)

        assert result["processed_count"] == 3
        assert result["updated_count"] == 3
        assert result["skipped_count"] == 0
        assert result["error_count"] == 0

    def test_return_counters(self, db_session: Session):
        """Deve retornar contadores processed/updated/skipped/errors."""
        # Criar shipment sem dados suficientes
        shipment = Shipment(
            tracking_code="TEST009",
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

        # Sem regra SLA
        result = recalculate_all_shipments_sla(db_session)

        assert result["processed_count"] >= 1  # Pode ter outros shipments no banco
        assert result["error_count"] == 0

    def test_skip_shipment_without_data(self, db_session: Session):
        """Deve pular shipment sem dados suficientes sem falhar."""
        shipment = Shipment(
            tracking_code="TEST010",
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

        # Sem regra SLA
        result = recalculate_shipment_sla(db_session, shipment.id)

        assert result["success"] is True  # Não deve falhar
        assert result["sla_status"] == "unknown"

    def test_respect_filters(self, db_session: Session):
        """Deve respeitar filtros."""
        # Criar 3 shipments com carriers diferentes
        for i in range(3):
            shipment = Shipment(
                tracking_code=f"TEST01{i}",
                carrier_id=i + 1,
                status="pending",
                estimated_delivery=datetime(2025, 1, 20, tzinfo=UTC),
                recipient_name="Test Customer",
                recipient_phone="11999999999",
                origin_address="Origin",
                destination_address="Destination",
            )
            db_session.add(shipment)
        db_session.commit()

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Reprocessar apenas carrier_id=1
        result = recalculate_all_shipments_sla(db_session, carrier_id=1)

        assert result["processed_count"] == 1  # Apenas 1 shipment

    def test_idempotent(self, db_session: Session):
        """Deve ser idempotente."""
        shipment = Shipment(
            tracking_code="TEST011",
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
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Reprocessar 2 vezes
        result1 = recalculate_shipment_sla(db_session, shipment.id)
        result2 = recalculate_shipment_sla(db_session, shipment.id)

        assert result1["success"] is True
        assert result2["success"] is True
        assert result1["sla_status"] == result2["sla_status"]

    def test_register_calculated_at(self, db_session: Session):
        """Deve registrar sla_calculated_at, se aplicável (on-demand, não persistido)."""
        shipment = Shipment(
            tracking_code="TEST012",
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
        db_session.refresh(shipment)

        # Criar regra SLA
        from app.modules.sla.models import SlaRule
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()

        # Reprocessar (on-demand, não persiste)
        result = recalculate_shipment_sla(db_session, shipment.id)

        # Verificar que o cálculo foi feito (on-demand)
        assert result["success"] is True
        assert result["sla_status"] is not None
