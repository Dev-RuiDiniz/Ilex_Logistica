import pytest

from tests.conftest import create_user_with_roles, login


PRIVATE_ROUTES = [
    ("post", "/api/v1/orders/imports/preview", {"files": {"file": ("orders.csv", b"x", "text/csv")}}),
    ("post", "/api/v1/orders/imports/confirm", {"json": {"import_id": 1}}),
    ("get", "/api/v1/orders/imports/1", {}),
    ("get", "/api/v1/orders", {}),
    ("get", "/api/v1/orders/1", {}),
    ("post", "/api/v1/orders/1/quote-rounds", {}),
    ("get", "/api/v1/orders/1/quote-rounds", {}),
    ("get", "/api/v1/quote-rounds/1", {}),
    ("post", "/api/v1/quote-rounds/1/quotes", {"json": {"carrier_id": 1, "status": "error"}}),
    ("post", "/api/v1/quote-rounds/1/quotes/import/preview", {"files": {"file": ("quotes.csv", b"x", "text/csv")}}),
    ("post", "/api/v1/quote-rounds/1/quotes/import/confirm", {"json": {"import_id": 1}}),
    ("post", "/api/v1/quote-rounds/1/select/1", {"json": {"reason": "justificativa valida"}}),
]


@pytest.mark.parametrize(("method", "path", "kwargs"), PRIVATE_ROUTES)
def test_orders_private_routes_return_401_without_session(client, method, path, kwargs) -> None:
    response = getattr(client, method)(path, **kwargs)
    assert response.status_code == 401


@pytest.mark.parametrize(("method", "path", "kwargs"), PRIVATE_ROUTES)
def test_orders_private_routes_return_403_without_permission(
    client, db_session, seed_roles, method, path, kwargs
) -> None:
    from app.modules.users.models import Role

    db_session.add(Role(name="sem_acesso"))
    db_session.commit()
    create_user_with_roles(db_session, "blocked@example.com", "test123", ["sem_acesso"])
    token = login(client, "blocked@example.com", "test123")
    response = getattr(client, method)(path, headers={"Authorization": f"Bearer {token}"}, **kwargs)
    assert response.status_code == 403
