"""add whatsapp and email to carriers

Revision ID: 20260702_01
Revises: 20260701_02
Create Date: 2026-07-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260702_01'
down_revision: Union[str, None] = '20260701_02'
branch_labels: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'carriers',
        sa.Column('whatsapp', sa.String(length=30), nullable=True),
    )
    op.add_column(
        'carriers',
        sa.Column('email', sa.String(length=120), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('carriers', 'email')
    op.drop_column('carriers', 'whatsapp')
