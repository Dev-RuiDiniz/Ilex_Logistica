"""Create operational_audit_logs table for BETA-019A.

Revision ID: 20260622_01
Revises: 20260621_01
Create Date: 2025-01-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260622_01'
down_revision: Union[str, None] = '20260621_01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create operational_audit_logs table."""
    op.create_table(
        'operational_audit_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=20), nullable=False),
        sa.Column('actor_user_id', sa.Integer(), nullable=True),
        sa.Column('actor_email', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('before_json', sa.Text(), nullable=True),
        sa.Column('after_json', sa.Text(), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('request_id', sa.String(length=100), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['actor_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operational_audit_logs_action'), 'operational_audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_actor_email'), 'operational_audit_logs', ['actor_email'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_actor_user_id'), 'operational_audit_logs', ['actor_user_id'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_created_at'), 'operational_audit_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_entity_id'), 'operational_audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_entity_type'), 'operational_audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_event_type'), 'operational_audit_logs', ['event_type'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_severity'), 'operational_audit_logs', ['severity'], unique=False)
    op.create_index(op.f('ix_operational_audit_logs_status'), 'operational_audit_logs', ['status'], unique=False)


def downgrade() -> None:
    """Drop operational_audit_logs table."""
    op.drop_index(op.f('ix_operational_audit_logs_status'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_severity'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_event_type'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_entity_type'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_entity_id'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_created_at'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_actor_user_id'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_actor_email'), table_name='operational_audit_logs')
    op.drop_index(op.f('ix_operational_audit_logs_action'), table_name='operational_audit_logs')
    op.drop_table('operational_audit_logs')
