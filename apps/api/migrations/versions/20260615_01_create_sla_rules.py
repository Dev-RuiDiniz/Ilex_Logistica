"""create sla_rules table

Revision ID: 20260615_01
Revises: 20260610_01
Create Date: 2025-06-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20260615_01'
down_revision: Union[str, None] = '20260610_01'
branch_labels: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sla_rules table
    op.create_table(
        'sla_rules',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('carrier_id', sa.Integer(), nullable=True),
        sa.Column('destination_uf', sa.String(length=2), nullable=True),
        sa.Column('transit_days', sa.Integer(), nullable=False),
        sa.Column('warning_threshold_days', sa.Integer(), nullable=False),
        sa.Column('critical_delay_days', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['carrier_id'], ['carriers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sla_rules_carrier_id', 'sla_rules', ['carrier_id'], unique=False)
    op.create_index('ix_sla_rules_destination_uf', 'sla_rules', ['destination_uf'], unique=False)
    op.create_index('ix_sla_rules_is_active', 'sla_rules', ['is_active'], unique=False)


def downgrade() -> None:
    # Drop sla_rules table
    op.drop_index('ix_sla_rules_is_active', table_name='sla_rules')
    op.drop_index('ix_sla_rules_destination_uf', table_name='sla_rules')
    op.drop_index('ix_sla_rules_carrier_id', table_name='sla_rules')
    op.drop_table('sla_rules')
