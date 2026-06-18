"""Merge alert and RBAC migration branches for BETA-027.

Revision ID: 20260627_01
Revises: 20260624_01, 20260620_02
Create Date: 2026-06-27

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = '20260627_01'
down_revision: Union[str, Sequence[str], None] = ('20260624_01', '20260620_02')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge both migration branches without altering schema."""
    return None


def downgrade() -> None:
    """Undoing a merge revision has no schema effect."""
    return None
