"""Seed de usuarios padrao para desenvolvimento e homologacao local."""

from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.models import Role, User
from app.modules.users.seed_permissions import seed_role_permissions

DEFAULT_DEV_PASSWORD = "123456"
DEFAULT_DEV_USERS: list[dict[str, str | list[str]]] = [
    {
        "email": "admin@ilex.com",
        "full_name": "Administrador Ilex",
        "roles": ["admin"],
    },
    {
        "email": "manager@ilex.com",
        "full_name": "Manager Operacional Ilex",
        "roles": ["manager"],
    },
    {
        "email": "operator@ilex.com",
        "full_name": "Operador Ilex",
        "roles": ["operator"],
    },
    {
        "email": "viewer@ilex.com",
        "full_name": "Viewer Ilex",
        "roles": ["viewer"],
    },
    {
        "email": "logistica@ilex.com",
        "full_name": "Logistica Ilex",
        "roles": ["logistica"],
    },
    {
        "email": "gestor@ilex.com",
        "full_name": "Gestor Ilex",
        "roles": ["gestor"],
    },
    {
        "email": "audit@ilex.com",
        "full_name": "Auditoria Ilex",
        "roles": ["auditoria"],
    },
]


def _ensure_roles(db: Session, role_names: Sequence[str]) -> None:
    for role_name in role_names:
        existing = db.query(Role).filter(Role.name == role_name).first()
        if existing is None:
            db.add(Role(name=role_name))
    db.commit()
    seed_role_permissions(db)


def seed_dev_users(db: Session) -> dict[str, int]:
    role_names = sorted({role for user in DEFAULT_DEV_USERS for role in user["roles"]})  # type: ignore[index]
    _ensure_roles(db, role_names)

    created = 0
    updated = 0

    for seed in DEFAULT_DEV_USERS:
        email = str(seed["email"])
        full_name = str(seed["full_name"])
        requested_roles = list(seed["roles"])  # type: ignore[arg-type]

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            user = User(
                email=email,
                full_name=full_name,
                password_hash=hash_password(DEFAULT_DEV_PASSWORD),
                is_active=True,
            )
            db.add(user)
            db.flush()
            created += 1
        else:
            user.full_name = full_name
            user.password_hash = hash_password(DEFAULT_DEV_PASSWORD)
            user.is_active = True
            updated += 1

        roles = db.query(Role).filter(Role.name.in_(requested_roles)).all()
        user.roles.clear()
        user.roles.extend(roles)

    db.commit()
    return {"created": created, "updated": updated}
