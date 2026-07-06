"""create orders and freight quotes domain

Revision ID: 20260703_02
Revises: 20260703_01
"""

from alembic import op
import sqlalchemy as sa

revision = "20260703_02"
down_revision = "20260703_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("external_number", sa.String(100), nullable=False),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("customer_name", sa.String(255), nullable=False),
        sa.Column("origin_zip", sa.String(8), nullable=False),
        sa.Column("origin_uf", sa.String(2), nullable=False),
        sa.Column("destination_zip", sa.String(8), nullable=False),
        sa.Column("destination_uf", sa.String(2), nullable=False),
        sa.Column("weight_kg", sa.Numeric(12, 3), nullable=False),
        sa.Column("volume_count", sa.Integer(), nullable=False),
        sa.Column("goods_value", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("import_history_id", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["import_history_id"], ["import_histories.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "external_number", name="uq_orders_source_external_number"),
    )
    op.create_index("ix_orders_order_date", "orders", ["order_date"])
    op.create_index("ix_orders_status", "orders", ["status"])
    op.create_index("ix_orders_status_order_date", "orders", ["status", "order_date"])
    op.create_index("ix_orders_import_history_id", "orders", ["import_history_id"])
    op.create_index("ix_orders_created_at", "orders", ["created_at"])

    op.create_table(
        "quote_rounds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("recommended_quote_id", sa.Integer(), nullable=True),
        sa.Column("selected_quote_id", sa.Integer(), nullable=True),
        sa.Column("selection_mode", sa.String(20), nullable=True),
        sa.Column("selection_reason", sa.Text(), nullable=True),
        sa.Column("selected_by", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["selected_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id", "sequence", name="uq_quote_rounds_order_sequence"),
    )
    op.create_index("ix_quote_rounds_order_id", "quote_rounds", ["order_id"])
    op.create_index("ix_quote_rounds_status", "quote_rounds", ["status"])
    op.create_index("ix_quote_rounds_expires_at", "quote_rounds", ["expires_at"])
    op.create_index("ix_quote_rounds_status_expires_at", "quote_rounds", ["status", "expires_at"])
    op.create_index("ix_quote_rounds_created_at", "quote_rounds", ["created_at"])

    op.create_table(
        "freight_quotes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("round_id", sa.Integer(), nullable=False),
        sa.Column("carrier_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("transit_days", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["round_id"], ["quote_rounds.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["carrier_id"], ["carriers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("round_id", "carrier_id", name="uq_freight_quotes_round_carrier"),
    )
    op.create_index("ix_freight_quotes_round_id", "freight_quotes", ["round_id"])
    op.create_index("ix_freight_quotes_carrier_id", "freight_quotes", ["carrier_id"])
    op.create_index("ix_freight_quotes_status", "freight_quotes", ["status"])
    op.create_index("ix_freight_quotes_valid_until", "freight_quotes", ["valid_until"])
    op.create_index("ix_freight_quotes_status_valid_until", "freight_quotes", ["status", "valid_until"])
    op.create_index("ix_freight_quotes_created_at", "freight_quotes", ["created_at"])
    with op.batch_alter_table("quote_rounds") as batch_op:
        batch_op.create_foreign_key(
            "fk_quote_rounds_recommended_quote_id",
            "freight_quotes",
            ["recommended_quote_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_foreign_key(
            "fk_quote_rounds_selected_quote_id",
            "freight_quotes",
            ["selected_quote_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("quote_rounds") as batch_op:
        batch_op.drop_constraint("fk_quote_rounds_selected_quote_id", type_="foreignkey")
        batch_op.drop_constraint("fk_quote_rounds_recommended_quote_id", type_="foreignkey")
    op.drop_table("freight_quotes")
    op.drop_table("quote_rounds")
    op.drop_table("orders")
