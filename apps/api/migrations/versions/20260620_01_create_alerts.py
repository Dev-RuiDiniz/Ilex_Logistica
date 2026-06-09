"""Create alerts table for BETA-017A.

Revision ID: 20260620_01
Revises: 20260615_01
Create Date: 2025-01-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260620_01'
down_revision: Union[str, None] = '20260615_01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create alerts table."""
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('shipment_id', sa.Integer(), nullable=True),
        sa.Column('carrier_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['carrier_id'], ['carriers.id'], ),
        sa.ForeignKeyConstraint(['shipment_id'], ['shipments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_alert_type'), 'alerts', ['alert_type'], unique=False)
    op.create_index(op.f('ix_alerts_carrier_id'), 'alerts', ['carrier_id'], unique=False)
    op.create_index(op.f('ix_alerts_generated_at'), 'alerts', ['generated_at'], unique=False)
    op.create_index(op.f('ix_alerts_severity'), 'alerts', ['severity'], unique=False)
    op.create_index(op.f('ix_alerts_shipment_id'), 'alerts', ['shipment_id'], unique=False)
    op.create_index(op.f('ix_alerts_source_id'), 'alerts', ['source_id'], unique=False)
    op.create_index(op.f('ix_alerts_source_type'), 'alerts', ['source_type'], unique=False)
    op.create_index(op.f('ix_alerts_status'), 'alerts', ['status'], unique=False)


def downgrade() -> None:
    """Drop alerts table."""
    op.drop_index(op.f('ix_alerts_status'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_source_type'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_source_id'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_shipment_id'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_severity'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_generated_at'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_carrier_id'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_alert_type'), table_name='alerts')
    op.drop_table('alerts')
