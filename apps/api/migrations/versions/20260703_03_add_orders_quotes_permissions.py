"""add orders and quotes permissions

Revision ID: 20260703_03
Revises: 20260703_02
"""

from alembic import op

revision = "20260703_03"
down_revision = "20260703_02"
branch_labels = None
depends_on = None

PERMISSIONS = (
    ("orders:read", "Read ERP orders", "orders", "read"),
    ("orders:write", "Import and update ERP orders", "orders", "write"),
    ("quotes:read", "Read freight quotes", "quotes", "read"),
    ("quotes:write", "Record freight quotes", "quotes", "write"),
    ("quotes:override", "Override recommended freight quote", "quotes", "override"),
)
ROLE_MATRIX = {
    "orders:read": ("admin", "manager", "operator", "viewer", "logistica", "gestor", "auditoria"),
    "orders:write": ("admin", "operator", "logistica"),
    "quotes:read": ("admin", "manager", "operator", "viewer", "logistica", "gestor", "auditoria"),
    "quotes:write": ("admin", "operator", "logistica"),
    "quotes:override": ("admin", "manager", "gestor"),
}


def upgrade() -> None:
    for name, description, resource, action in PERMISSIONS:
        op.execute(
            "INSERT INTO permissions (name, description, resource, action) "
            f"VALUES ('{name}', '{description}', '{resource}', '{action}')"
        )
    for permission, roles in ROLE_MATRIX.items():
        role_list = ", ".join(f"'{role}'" for role in roles)
        op.execute(
            "INSERT INTO role_permissions (role_id, permission_id) "
            "SELECT roles.id, permissions.id FROM roles CROSS JOIN permissions "
            f"WHERE roles.name IN ({role_list}) AND permissions.name = '{permission}' "
            "AND NOT EXISTS (SELECT 1 FROM role_permissions current "
            "WHERE current.role_id = roles.id AND current.permission_id = permissions.id)"
        )


def downgrade() -> None:
    names = ", ".join(f"'{name}'" for name, *_ in PERMISSIONS)
    op.execute(
        "DELETE FROM role_permissions WHERE permission_id IN "
        f"(SELECT id FROM permissions WHERE name IN ({names}))"
    )
    op.execute(f"DELETE FROM permissions WHERE name IN ({names})")
