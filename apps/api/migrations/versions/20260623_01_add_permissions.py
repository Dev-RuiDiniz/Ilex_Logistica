"""Add permissions model and role_permissions table for RBAC.

Revision ID: 20260623_01_add_permissions
Revises: 20260622_01_create_operational_audit_logs
Create Date: 2025-01-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260623_01"
down_revision: Union[str, None] = "20260622_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create permissions table
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("resource", sa.String(length=50), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_permissions_name"), "permissions", ["name"], unique=True)
    op.create_index(op.f("ix_permissions_resource"), "permissions", ["resource"], unique=False)

    # Create role_permissions table
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )

    # Insert default permissions
    op.execute(
        """
        INSERT INTO permissions (name, description, resource, action) VALUES
        ('shipments:read', 'Read shipments', 'shipments', 'read'),
        ('shipments:write', 'Write shipments', 'shipments', 'write'),
        ('imports:read', 'Read imports', 'imports', 'read'),
        ('imports:write', 'Write imports', 'imports', 'write'),
        ('sla:read', 'Read SLA rules', 'sla', 'read'),
        ('sla:write', 'Write SLA rules', 'sla', 'write'),
        ('alerts:read', 'Read alerts', 'alerts', 'read'),
        ('alerts:write', 'Write alerts', 'alerts', 'write'),
        ('reports:read', 'Read reports', 'reports', 'read'),
        ('reports:write', 'Write reports', 'reports', 'write'),
        ('audit:read', 'Read audit logs', 'audit', 'read'),
        ('users:read', 'Read users', 'users', 'read'),
        ('users:write', 'Write users', 'users', 'write')
        """
    )


def downgrade() -> None:
    op.drop_table("role_permissions")
    op.drop_index(op.f("ix_permissions_resource"), table_name="permissions")
    op.drop_index(op.f("ix_permissions_name"), table_name="permissions")
    op.drop_table("permissions")
