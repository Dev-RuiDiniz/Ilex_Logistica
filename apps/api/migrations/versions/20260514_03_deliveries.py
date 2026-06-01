"""deliveries table for fiscal and financial fields

Revision ID: 20260514_03
Revises: 20260514_02
Create Date: 2026-05-14
"""

from alembic import op
import sqlalchemy as sa

revision = "20260514_03"
down_revision = "20260514_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "deliveries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nf", sa.String(length=64), nullable=False),
        sa.Column("transportadora", sa.String(length=255), nullable=False),
        sa.Column("data_coleta", sa.Date(), nullable=False),
        sa.Column("valor_frete", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("percentual_frete", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deliveries_nf"), "deliveries", ["nf"], unique=False)
    op.create_index(op.f("ix_deliveries_data_coleta"), "deliveries", ["data_coleta"], unique=False)
    op.create_index(op.f("ix_deliveries_created_at"), "deliveries", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_deliveries_created_at"), table_name="deliveries")
    op.drop_index(op.f("ix_deliveries_data_coleta"), table_name="deliveries")
    op.drop_index(op.f("ix_deliveries_nf"), table_name="deliveries")
    op.drop_table("deliveries")
