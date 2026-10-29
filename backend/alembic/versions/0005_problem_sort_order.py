"""problems: sort_order for the learning path

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-08
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "problems",
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_index("ix_problems_sort_order", "problems", ["sort_order"])


def downgrade() -> None:
    op.drop_index("ix_problems_sort_order", table_name="problems")
    op.drop_column("problems", "sort_order")
