"""Create daily_reports table for BETA-018A.

Revision ID: 20260621_01
Revises: 20260620_01
Create Date: 2025-01-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260621_01'
down_revision: Union[str, None] = '20260620_01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create daily_reports table."""
    op.create_table(
        'daily_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('report_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='generated'),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
        sa.Column('generated_by_user_id', sa.Integer(), nullable=True),
        sa.Column('period_start', sa.DateTime(), nullable=True),
        sa.Column('period_end', sa.DateTime(), nullable=True),
        sa.Column('summary_json', sa.Text(), nullable=True),
        sa.Column('kpis_json', sa.Text(), nullable=True),
        sa.Column('exceptions_json', sa.Text(), nullable=True),
        sa.Column('alerts_json', sa.Text(), nullable=True),
        sa.Column('carrier_efficiency_json', sa.Text(), nullable=True),
        sa.Column('import_failures_json', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_date')
    )
    op.create_index(op.f('ix_daily_reports_generated_at'), 'daily_reports', ['generated_at'], unique=False)
    op.create_index(op.f('ix_daily_reports_generated_by_user_id'), 'daily_reports', ['generated_by_user_id'], unique=False)
    op.create_index(op.f('ix_daily_reports_report_date'), 'daily_reports', ['report_date'], unique=False)
    op.create_index(op.f('ix_daily_reports_status'), 'daily_reports', ['status'], unique=False)


def downgrade() -> None:
    """Drop daily_reports table."""
    op.drop_index(op.f('ix_daily_reports_status'), table_name='daily_reports')
    op.drop_index(op.f('ix_daily_reports_report_date'), table_name='daily_reports')
    op.drop_index(op.f('ix_daily_reports_generated_by_user_id'), table_name='daily_reports')
    op.drop_index(op.f('ix_daily_reports_generated_at'), table_name='daily_reports')
    op.drop_table('daily_reports')
