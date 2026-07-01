"""add imported_count and rejected_count to import_histories

Revision ID: 20260701_02
Revises: 20260701_01
Create Date: 2026-07-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260701_02'
down_revision: Union[str, None] = '20260701_01'
branch_labels: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'import_histories',
        sa.Column('imported_count', sa.Integer(), nullable=False, server_default='0'),
    )
    op.add_column(
        'import_histories',
        sa.Column('rejected_count', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    op.drop_column('import_histories', 'rejected_count')
    op.drop_column('import_histories', 'imported_count')
