from pathlib import Path

from sqlalchemy.orm import Session

from tests.conftest import create_user_with_roles, login
from app.modules.orders.models import Order


CSV_HEADER = (
    "source,external_number,order_date,customer_name,origin_zip,origin_uf,"
    "destination_zip,destination_uf,weight_kg,volume_count,goods_value,currency\n"
)
CSV_ROW = "erp,PED-1,2026-07-03,Cliente,01310100,SP,20040002,RJ,10.5,2,1200.00,BRL\n"


def test_order_import_preview_then_confirm_is_idempotent(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    preview = client.post(
        "/api/v1/orders/imports/preview",
        headers=auth_headers,
        files={"file": ("orders.csv", (CSV_HEADER + CSV_ROW).encode(), "text/csv")},
    )
    assert preview.status_code == 200
    body = preview.json()
    assert body["valid_rows"] == 1
    assert body["invalid_rows"] == 0
    assert db_session.query(Order).count() == 0

    first = client.post(
        "/api/v1/orders/imports/confirm",
        headers=auth_headers,
        json={"import_id": body["import_id"]},
    )
    second = client.post(
        "/api/v1/orders/imports/confirm",
        headers=auth_headers,
        json={"import_id": body["import_id"]},
    )
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["imported_count"] == 1
    assert db_session.query(Order).count() == 1


def test_order_import_reports_line_errors_without_persisting_invalid_row(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    invalid = "erp,PED-2,2026-07-03,Cliente,123,XX,20040002,RJ,-1,0,0,USD\n"
    preview = client.post(
        "/api/v1/orders/imports/preview",
        headers=auth_headers,
        files={"file": ("orders.csv", (CSV_HEADER + CSV_ROW + invalid).encode(), "text/csv")},
    )
    assert preview.status_code == 200
    body = preview.json()
    assert body["valid_rows"] == 1
    assert body["invalid_rows"] == 1
    assert {error["row_number"] for error in body["errors"]} == {3}

    confirmed = client.post(
        "/api/v1/orders/imports/confirm",
        headers=auth_headers,
        json={"import_id": body["import_id"]},
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["imported_count"] == 1
    assert confirmed.json()["rejected_count"] == 1
    assert db_session.query(Order).count() == 1


def test_order_import_requires_authentication(client) -> None:
    response = client.post(
        "/api/v1/orders/imports/preview",
        files={"file": ("orders.csv", (CSV_HEADER + CSV_ROW).encode(), "text/csv")},
    )
    assert response.status_code == 401


def test_order_import_rejects_write_for_read_only_profile(client, db_session, seed_roles) -> None:
    create_user_with_roles(db_session, "viewer@example.com", "test123", ["viewer"])
    headers = {"Authorization": f"Bearer {login(client, 'viewer@example.com', 'test123')}"}
    response = client.post(
        "/api/v1/orders/imports/preview",
        headers=headers,
        files={"file": ("orders.csv", (CSV_HEADER + CSV_ROW).encode(), "text/csv")},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "sem permissao: orders:write"


def test_order_import_updates_importable_fields_without_duplicating_order(
    client, auth_headers: dict[str, str], db_session: Session
) -> None:
    def import_csv(row: str) -> None:
        preview = client.post(
            "/api/v1/orders/imports/preview",
            headers=auth_headers,
            files={"file": ("orders.csv", (CSV_HEADER + row).encode(), "text/csv")},
        )
        assert preview.status_code == 200
        confirmed = client.post(
            "/api/v1/orders/imports/confirm",
            headers=auth_headers,
            json={"import_id": preview.json()["import_id"]},
        )
        assert confirmed.status_code == 200

    import_csv(CSV_ROW)
    import_csv(CSV_ROW.replace("Cliente", "Cliente Atualizado").replace("1200.00", "1300.00"))

    assert db_session.query(Order).count() == 1
    order = db_session.query(Order).one()
    assert order.customer_name == "Cliente Atualizado"
    assert str(order.goods_value) == "1300.00"

    listed = client.get("/api/v1/orders?external_number=PED-1", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.json()["total"] == 1


def test_order_import_accepts_sanitized_xlsx_fixture(client, auth_headers: dict[str, str]) -> None:
    fixture = Path(__file__).parent / "fixtures" / "orders" / "orders_10.xlsx"
    preview = client.post(
        "/api/v1/orders/imports/preview",
        headers=auth_headers,
        files={
            "file": (
                fixture.name,
                fixture.read_bytes(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert preview.status_code == 200
    assert preview.json()["valid_rows"] == 10
