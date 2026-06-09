"""add metadata fields to import_histories - BETA-012A

Revision ID: 20260610_01
Revises: 20260608_01
Create Date: 2026-06-10
"""

from alembic import op
import sqlalchemy as sa


revision = "20260610_01"
down_revision = "20260608_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add source field
    op.add_column(
        "import_histories",
        sa.Column("source", sa.String(length=50), nullable=True),
    )
    
    # Add import_metadata field (JSON stored as text)
    op.add_column(
        "import_histories",
        sa.Column("import_metadata", sa.Text(), nullable=True),
    )
    
    # Add imported_by field (foreign key to users)
    op.add_column(
        "import_histories",
        sa.Column("imported_by", sa.Integer(), nullable=True),
    )
    
    # Create index on imported_by
    op.create_index("ix_import_histories_imported_by", "import_histories", ["imported_by"])


def downgrade() -> None:
    # Drop index
    op.drop_index("ix_import_histories_imported_by", table_name="import_histories")
    
    # Drop columns
    op.drop_column("import_histories", "imported_by")
    op.drop_column("import_histories", "import_metadata")
    op.drop_column("import_histories", "source")
