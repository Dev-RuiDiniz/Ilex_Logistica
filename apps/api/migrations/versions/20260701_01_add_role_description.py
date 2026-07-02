"""add description column to roles

Revision ID: 20260701_01
Revises: cbee64373bd6
Create Date: 2026-07-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260701_01'
down_revision: Union[str, None] = 'cbee64373bd6'
branch_labels: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('roles', sa.Column('description', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('roles', 'description')
