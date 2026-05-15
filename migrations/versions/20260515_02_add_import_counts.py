"""add imported_count and rejected_count to import_history

Revision ID: 20260515_02
Revises: 20260515_01
Create Date: 2026-05-15
"""

from alembic import op
import sqlalchemy as sa

revision = "20260515_02"
down_revision = "20260515_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "import_history",
        sa.Column("imported_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "import_history",
        sa.Column("rejected_count", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("import_history", "rejected_count")
    op.drop_column("import_history", "imported_count")
