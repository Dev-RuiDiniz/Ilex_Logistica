"""Add carriers permissions for RBAC.

Revision ID: 20260624_01_add_carriers_permissions
Revises: 20260623_01
Create Date: 2025-01-22

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20260624_01"
down_revision: Union[str, None] = "20260623_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert carriers permissions
    op.execute(
        """
        INSERT INTO permissions (name, description, resource, action) VALUES
        ('carriers:read', 'Read carriers', 'carriers', 'read'),
        ('carriers:write', 'Write carriers', 'carriers', 'write')
        """
    )


def downgrade() -> None:
    # Remove carriers permissions
    op.execute(
        """
        DELETE FROM permissions WHERE name IN ('carriers:read', 'carriers:write')
        """
    )
