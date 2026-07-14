"""add role description

Revision ID: 20260627_02
Revises: 20260627_01
Create Date: 2026-06-17
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20260627_02"
down_revision = "20260627_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in inspect(bind).get_columns("roles")}
    if "description" not in columns:
        op.add_column("roles", sa.Column("description", sa.String(length=255), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in inspect(bind).get_columns("roles")}
    if "description" in columns:
        op.drop_column("roles", "description")
