"""Testes para regras SLA - BETA-013A."""

from datetime import UTC, datetime
from sqlalchemy.orm import Session

from app.modules.sla.models import SlaRule
from app.modules.sla.service import (
    get_applicable_sla_rule,
    calculate_sla_due_date,
    calculate_sla_status,
    calculate_delay_days_sla,
    calculate_criticality_sla,
)


class TestSlaRuleModel:
    """Testes do modelo SlaRule."""

    def test_create_sla_rule_global(self, db_session: Session):
        """Deve criar regra SLA global/default."""
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)

        assert rule.id is not None
        assert rule.carrier_id is None
        assert rule.destination_uf is None
        assert rule.transit_days == 5
        assert rule.warning_threshold_days == 2
        assert rule.critical_delay_days == 3
        assert rule.is_active is True

    def test_create_sla_rule_by_carrier(self, db_session: Session):
        """Deve criar regra SLA por transportadora."""
        rule = SlaRule(
            carrier_id=1,
            transit_days=7,
            warning_threshold_days=3,
            critical_delay_days=5,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)

        assert rule.carrier_id == 1
        assert rule.destination_uf is None

    def test_create_sla_rule_by_carrier_and_uf(self, db_session: Session):
        """Deve criar regra SLA por transportadora + UF."""
        rule = SlaRule(
            carrier_id=1,
            destination_uf="SP",
            transit_days=3,
            warning_threshold_days=1,
            critical_delay_days=2,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)

        assert rule.carrier_id == 1
        assert rule.destination_uf == "SP"

    def test_validate_transit_days_positive(self, db_session: Session):
        """Deve validar transit_days positivo."""
        rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)

        assert rule.transit_days > 0

    def test_validate_uf_two_letters(self, db_session: Session):
        """Deve validar UF com 2 letras quando informada."""
        rule = SlaRule(
            destination_uf="SP",
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(rule)
        db_session.commit()
        db_session.refresh(rule)

        assert len(rule.destination_uf) == 2
        assert rule.destination_uf.isupper()


class TestSlaRulePriority:
    """Testes de prioridade de regras SLA."""

    def test_prioritize_carrier_uf_rule(self, db_session: Session):
        """Deve priorizar regra transportadora + UF."""
        # Criar regra global
        global_rule = SlaRule(
            transit_days=10,
            warning_threshold_days=5,
            critical_delay_days=7,
            is_active=True,
        )
        db_session.add(global_rule)

        # Criar regra por transportadora
        carrier_rule = SlaRule(
            carrier_id=1,
            transit_days=7,
            warning_threshold_days=3,
            critical_delay_days=5,
            is_active=True,
        )
        db_session.add(carrier_rule)

        # Criar regra por transportadora + UF
        carrier_uf_rule = SlaRule(
            carrier_id=1,
            destination_uf="SP",
            transit_days=3,
            warning_threshold_days=1,
            critical_delay_days=2,
            is_active=True,
        )
        db_session.add(carrier_uf_rule)
        db_session.commit()

        # Buscar regra aplicável para carrier_id=1, UF=SP
        rule = get_applicable_sla_rule(db_session, carrier_id=1, destination_uf="SP")

        assert rule is not None
        assert rule.transit_days == 3  # Deve usar a regra mais específica
        assert rule.carrier_id == 1
        assert rule.destination_uf == "SP"

    def test_fallback_to_carrier_rule(self, db_session: Session):
        """Deve usar fallback por transportadora."""
        # Criar regra global
        global_rule = SlaRule(
            transit_days=10,
            warning_threshold_days=5,
            critical_delay_days=7,
            is_active=True,
        )
        db_session.add(global_rule)

        # Criar regra por transportadora
        carrier_rule = SlaRule(
            carrier_id=1,
            transit_days=7,
            warning_threshold_days=3,
            critical_delay_days=5,
            is_active=True,
        )
        db_session.add(carrier_rule)
        db_session.commit()

        # Buscar regra aplicável para carrier_id=1, UF=RJ (sem regra específica)
        rule = get_applicable_sla_rule(db_session, carrier_id=1, destination_uf="RJ")

        assert rule is not None
        assert rule.transit_days == 7  # Deve usar a regra por transportadora
        assert rule.carrier_id == 1
        assert rule.destination_uf is None

    def test_fallback_to_global_rule(self, db_session: Session):
        """Deve usar fallback global."""
        # Criar regra global
        global_rule = SlaRule(
            transit_days=10,
            warning_threshold_days=5,
            critical_delay_days=7,
            is_active=True,
        )
        db_session.add(global_rule)
        db_session.commit()

        # Buscar regra aplicável para carrier_id=2 (sem regra específica)
        rule = get_applicable_sla_rule(db_session, carrier_id=2, destination_uf="SP")

        assert rule is not None
        assert rule.transit_days == 10  # Deve usar a regra global
        assert rule.carrier_id is None
        assert rule.destination_uf is None

    def test_ignore_inactive_rule(self, db_session: Session):
        """Deve ignorar regra inativa."""
        # Criar regra global inativa
        inactive_rule = SlaRule(
            transit_days=10,
            warning_threshold_days=5,
            critical_delay_days=7,
            is_active=False,
        )
        db_session.add(inactive_rule)

        # Criar regra global ativa
        active_rule = SlaRule(
            transit_days=5,
            warning_threshold_days=2,
            critical_delay_days=3,
            is_active=True,
        )
        db_session.add(active_rule)
        db_session.commit()

        # Buscar regra aplicável
        rule = get_applicable_sla_rule(db_session, carrier_id=1, destination_uf="SP")

        assert rule is not None
        assert rule.transit_days == 5  # Deve usar a regra ativa
        assert rule.is_active is True

    def test_return_none_when_no_rule(self, db_session: Session):
        """Deve retornar None quando não houver regra."""
        rule = get_applicable_sla_rule(db_session, carrier_id=1, destination_uf="SP")
        assert rule is None


class TestSlaCalculation:
    """Testes de cálculo SLA."""

    def test_calculate_due_date_from_collection_date(self):
        """Deve calcular due date a partir de collection_departure_date + transit_days."""
        collection_date = datetime(2025, 1, 15, tzinfo=UTC)
        transit_days = 5

        due_date = calculate_sla_due_date(collection_date, transit_days)

        assert due_date == datetime(2025, 1, 20, tzinfo=UTC)

    def test_use_expected_delivery_when_exists(self):
        """Deve usar expected_delivery_date quando já existir."""
        expected_delivery = datetime(2025, 1, 20, tzinfo=UTC)
        collection_date = datetime(2025, 1, 15, tzinfo=UTC)
        transit_days = 5

        due_date = calculate_sla_due_date(collection_date, transit_days, expected_delivery)

        assert due_date == expected_delivery  # Deve usar expected_delivery

    def test_return_none_when_no_data(self):
        """Deve retornar None quando não houver dados suficientes."""
        due_date = calculate_sla_due_date(None, 5, None)
        assert due_date is None

    def test_calculate_delay_days_zero_on_time(self):
        """Deve calcular delay_days = 0 para entrega dentro do prazo."""
        sla_due_date = datetime(2025, 1, 20, tzinfo=UTC)
        delivered_at = datetime(2025, 1, 20, tzinfo=UTC)

        delay_days = calculate_delay_days_sla(sla_due_date, delivered_at)

        assert delay_days == 0

    def test_calculate_delay_days_correct_late(self):
        """Deve calcular delay_days correto para entrega atrasada."""
        sla_due_date = datetime(2025, 1, 20, tzinfo=UTC)
        delivered_at = datetime(2025, 1, 25, tzinfo=UTC)

        delay_days = calculate_delay_days_sla(sla_due_date, delivered_at)

        assert delay_days == 5

    def test_calculate_delay_with_delivered_at(self):
        """Deve calcular atraso com delivered_at quando entregue."""
        sla_due_date = datetime(2025, 1, 20, tzinfo=UTC)
        delivered_at = datetime(2025, 1, 25, tzinfo=UTC)

        delay_days = calculate_delay_days_sla(sla_due_date, delivered_at)

        assert delay_days == 5

    def test_calculate_delay_with_today_injectable(self):
        """Deve calcular atraso com today injetável quando não entregue."""
        sla_due_date = datetime(2025, 1, 20, tzinfo=UTC)
        today = datetime(2025, 1, 25, tzinfo=UTC)

        delay_days = calculate_delay_days_sla(sla_due_date, None, today)

        assert delay_days == 5

    def test_no_negative_delay(self):
        """Deve não retornar atraso negativo."""
        sla_due_date = datetime(2025, 1, 25, tzinfo=UTC)
        delivered_at = datetime(2025, 1, 20, tzinfo=UTC)

        delay_days = calculate_delay_days_sla(sla_due_date, delivered_at)

        assert delay_days == 0  # Deve ser 0, não negativo

    def test_classify_on_time(self):
        """Deve classificar on_time."""
        delay_days = 0
        warning_threshold = 2
        critical_threshold = 5

        status = calculate_sla_status(delay_days, warning_threshold, critical_threshold)

        assert status == "on_time"

    def test_classify_warning(self):
        """Deve classificar warning."""
        delay_days = 1
        warning_threshold = 2
        critical_threshold = 5

        status = calculate_sla_status(delay_days, warning_threshold, critical_threshold)

        assert status == "warning"

    def test_classify_late(self):
        """Deve classificar late."""
        delay_days = 3
        warning_threshold = 2
        critical_threshold = 5

        status = calculate_sla_status(delay_days, warning_threshold, critical_threshold)

        assert status == "late"

    def test_classify_critical(self):
        """Deve classificar critical."""
        delay_days = 6
        warning_threshold = 2
        critical_threshold = 5

        status = calculate_sla_status(delay_days, warning_threshold, critical_threshold)

        assert status == "critical"

    def test_respect_critical_threshold(self):
        """Deve respeitar threshold crítico configurado."""
        delay_days = 4
        warning_threshold = 2
        critical_threshold = 3

        status = calculate_sla_status(delay_days, warning_threshold, critical_threshold)

        assert status == "critical"  # 4 >= 3

    def test_return_unknown_when_no_due_date(self):
        """Deve retornar unknown quando não houver due_date."""
        status = calculate_sla_status(None, 2, 5)
        assert status == "unknown"

    def test_calculate_criticality_on_time(self):
        """Deve calcular criticality on_time."""
        delay_days = 0
        critical_threshold = 5

        criticality = calculate_criticality_sla(delay_days, critical_threshold)

        assert criticality == "normal"

    def test_calculate_criticality_late(self):
        """Deve calcular criticality late."""
        delay_days = 3
        critical_threshold = 5

        criticality = calculate_criticality_sla(delay_days, critical_threshold)

        assert criticality == "baixa"

    def test_calculate_criticality_critical(self):
        """Deve calcular criticality critical."""
        delay_days = 6
        critical_threshold = 5

        criticality = calculate_criticality_sla(delay_days, critical_threshold)

        assert criticality == "alta"
