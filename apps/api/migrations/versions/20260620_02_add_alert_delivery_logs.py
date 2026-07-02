"""Add alert delivery logs for BETA-017A.

Revision ID: 20260620_02
Revises: 20260620_01
Create Date: 2026-06-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260620_02'
down_revision: Union[str, None] = '20260620_01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create alert delivery logs table."""
    op.create_table(
        'alert_delivery_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('alert_id', sa.Integer(), nullable=False),
        sa.Column('channel', sa.String(length=20), nullable=False),
        sa.Column('recipient', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['alert_id'], ['alerts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_delivery_logs_alert_id'), 'alert_delivery_logs', ['alert_id'], unique=False)
    op.create_index(op.f('ix_alert_delivery_logs_channel'), 'alert_delivery_logs', ['channel'], unique=False)
    op.create_index(op.f('ix_alert_delivery_logs_created_at'), 'alert_delivery_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_alert_delivery_logs_status'), 'alert_delivery_logs', ['status'], unique=False)


def downgrade() -> None:
    """Drop alert delivery logs table."""
    op.drop_index(op.f('ix_alert_delivery_logs_status'), table_name='alert_delivery_logs')
    op.drop_index(op.f('ix_alert_delivery_logs_created_at'), table_name='alert_delivery_logs')
    op.drop_index(op.f('ix_alert_delivery_logs_channel'), table_name='alert_delivery_logs')
    op.drop_index(op.f('ix_alert_delivery_logs_alert_id'), table_name='alert_delivery_logs')
    op.drop_table('alert_delivery_logs')
