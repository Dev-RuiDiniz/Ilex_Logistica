"""import histories

Revision ID: 20260514_02
Revises: 20260513_01
Create Date: 2026-05-14
"""

from alembic import op
import sqlalchemy as sa

revision = "20260514_02"
down_revision = "20260513_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "import_histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=10), nullable=False),
        sa.Column("file_hash", sa.String(length=64), nullable=False),
        sa.Column("rows_received", sa.Integer(), nullable=False),
        sa.Column("duplicates_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_import_histories_created_at"), "import_histories", ["created_at"], unique=False)
    op.create_index(op.f("ix_import_histories_file_hash"), "import_histories", ["file_hash"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_import_histories_file_hash"), table_name="import_histories")
    op.drop_index(op.f("ix_import_histories_created_at"), table_name="import_histories")
    op.drop_table("import_histories")
