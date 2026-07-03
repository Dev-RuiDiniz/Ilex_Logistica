from pathlib import Path
from time import perf_counter

import pytest
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.modules.orders.models import Order
from app.modules.orders.service import confirm_order_import, preview_order_import


@pytest.mark.performance
def test_preview_and_confirm_ten_thousand_orders_within_sixty_seconds(db_session: Session, auth_headers) -> None:
    fixture = Path(__file__).parent / "fixtures" / "orders" / "orders_10000.csv"
    started = perf_counter()
    with fixture.open("rb") as stream:
        preview = preview_order_import(db_session, UploadFile(filename=fixture.name, file=stream), user_id=1)
    assert preview["valid_rows"] == 10_000
    result = confirm_order_import(db_session, preview["import_id"], user_id=1)
    elapsed = perf_counter() - started

    assert result.imported_count == 10_000
    assert db_session.query(Order).count() == 10_000
    assert elapsed <= 60, f"importacao levou {elapsed:.2f}s"
