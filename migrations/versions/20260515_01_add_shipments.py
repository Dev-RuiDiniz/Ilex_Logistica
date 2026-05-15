"""add shipments and import history

Revision ID: 20260515_01
Revises: 20260514_03
Create Date: 2026-05-15
"""

from alembic import op
import sqlalchemy as sa

revision = "20260515_01"
down_revision = "20260514_03"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "shipments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tracking_code", sa.String(length=100), nullable=False),
        sa.Column("carrier_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("estimated_delivery", sa.DateTime(), nullable=False),
        sa.Column("actual_delivery", sa.DateTime(), nullable=True),
        sa.Column("recipient_name", sa.String(length=255), nullable=False),
        sa.Column("recipient_phone", sa.String(length=50), nullable=False),
        sa.Column("origin_address", sa.Text(), nullable=False),
        sa.Column("destination_address", sa.Text(), nullable=False),
        sa.Column("meta_data", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["carrier_id"], ["carriers.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tracking_code"),
    )
    op.create_index(op.f("ix_shipments_tracking_code"), "shipments", ["tracking_code"], unique=False)
    op.create_index(op.f("ix_shipments_status"), "shipments", ["status"], unique=False)

    op.create_table(
        "import_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("valid_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("invalid_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_details", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("import_history")
    op.drop_index(op.f("ix_shipments_status"), table_name="shipments")
    op.drop_index(op.f("ix_shipments_tracking_code"), table_name="shipments")
    op.drop_table("shipments")
