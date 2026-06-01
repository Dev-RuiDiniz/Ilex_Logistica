"""add fiscal/financial fields to shipments

Revision ID: 20260515_04
Revises: 20260515_02
Create Date: 2026-05-15
"""

from alembic import op
import sqlalchemy as sa

revision = "20260515_04"
down_revision = "20260515_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("shipments", sa.Column("invoice_number", sa.String(length=50), nullable=True))
    op.add_column("shipments", sa.Column("invoice_key", sa.String(length=100), nullable=True))
    op.add_column("shipments", sa.Column("fiscal_document", sa.String(length=50), nullable=True))
    op.add_column("shipments", sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column("shipments", sa.Column("due_date", sa.DateTime(), nullable=True))
    op.add_column("shipments", sa.Column("delay_days", sa.Integer(), server_default="0", nullable=False))
    op.add_column("shipments", sa.Column("criticality", sa.String(length=20), server_default="normal", nullable=False))


def downgrade() -> None:
    op.drop_column("shipments", "criticality")
    op.drop_column("shipments", "delay_days")
    op.drop_column("shipments", "due_date")
    op.drop_column("shipments", "amount")
    op.drop_column("shipments", "fiscal_document")
    op.drop_column("shipments", "invoice_key")
    op.drop_column("shipments", "invoice_number")
