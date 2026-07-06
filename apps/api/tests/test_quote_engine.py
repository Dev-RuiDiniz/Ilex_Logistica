from datetime import UTC, datetime, timedelta
from decimal import Decimal

from app.modules.orders.models import FreightQuote
from app.modules.orders.quote_service import choose_best_quote


def _quote(quote_id: int, carrier_id: int, amount: str, days: int | None) -> FreightQuote:
    quote = FreightQuote(
        id=quote_id,
        carrier_id=carrier_id,
        round_id=1,
        amount=Decimal(amount),
        transit_days=days,
        status="quoted",
        valid_until=datetime.now(UTC) + timedelta(hours=1),
        created_by=1,
    )
    return quote


def test_choose_best_quote_uses_all_deterministic_tiebreakers() -> None:
    expensive = _quote(1, 1, "101.00", 1)
    no_deadline = _quote(2, 2, "100.00", None)
    less_efficient = _quote(3, 3, "100.00", 2)
    best = _quote(4, 4, "100.00", 2)
    stable_id = _quote(5, 5, "100.00", 2)

    selected = choose_best_quote(
        [expensive, no_deadline, less_efficient, best, stable_id],
        efficiencies={3: Decimal("90"), 4: Decimal("95"), 5: Decimal("95")},
        now=datetime.now(UTC),
    )
    assert selected is best


def test_choose_best_quote_ignores_failure_and_expired_results() -> None:
    valid = _quote(1, 1, "120.00", 3)
    failed = _quote(2, 2, "10.00", 1)
    failed.status = "error"
    expired = _quote(3, 3, "20.00", 1)
    expired.valid_until = datetime.now(UTC) - timedelta(seconds=1)

    assert choose_best_quote([failed, expired, valid], {}, datetime.now(UTC)) is valid
