from app.core.security import verify_password
from app.modules.users.models import User
from app.modules.users.seed_dev_users import DEFAULT_DEV_PASSWORD, DEFAULT_DEV_USERS, seed_dev_users


def test_seed_dev_users_cria_usuarios_padrao_com_roles(db_session, seed_roles) -> None:
    summary = seed_dev_users(db_session)

    assert summary["created"] == len(DEFAULT_DEV_USERS)
    assert summary["updated"] == 0

    users = db_session.query(User).order_by(User.email.asc()).all()
    assert len(users) == len(DEFAULT_DEV_USERS)

    user_map = {user.email: user for user in users}

    for seed in DEFAULT_DEV_USERS:
        user = user_map[seed["email"]]
        assert user.full_name == seed["full_name"]
        assert user.is_active is True
        assert sorted(role.name for role in user.roles) == sorted(seed["roles"])
        assert verify_password(DEFAULT_DEV_PASSWORD, user.password_hash)


def test_seed_dev_users_e_idempotente_e_restaura_roles(db_session, seed_roles) -> None:
    seed_dev_users(db_session)

    admin = db_session.query(User).filter(User.email == "admin@ilex.com").first()
    assert admin is not None
    admin.roles.clear()
    db_session.commit()

    summary = seed_dev_users(db_session)

    assert summary["created"] == 0
    assert summary["updated"] == len(DEFAULT_DEV_USERS)

    db_session.refresh(admin)
    assert sorted(role.name for role in admin.roles) == ["admin"]
    assert db_session.query(User).count() == len(DEFAULT_DEV_USERS)
