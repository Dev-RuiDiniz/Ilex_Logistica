from decimal import Decimal

from sqlalchemy import Numeric, UniqueConstraint

from app.modules.orders.models import FreightQuote, Order, QuoteRound


def _unique_columns(model: type) -> set[tuple[str, ...]]:
    return {
        tuple(column.name for column in constraint.columns)
        for constraint in model.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }


def test_order_contract_uses_decimal_and_natural_id() -> None:
    assert isinstance(Order.__table__.c.weight_kg.type, Numeric)
    assert isinstance(Order.__table__.c.goods_value.type, Numeric)
    assert ("source", "external_number") in _unique_columns(Order)

    order = Order(
        source="erp",
        external_number="PED-1",
        weight_kg=Decimal("10.500"),
        goods_value=Decimal("1200.00"),
    )
    assert order.goods_value == Decimal("1200.00")


def test_quote_round_and_quote_have_domain_uniqueness() -> None:
    assert ("order_id", "sequence") in _unique_columns(QuoteRound)
    assert ("round_id", "carrier_id") in _unique_columns(FreightQuote)
    assert isinstance(FreightQuote.__table__.c.amount.type, Numeric)
