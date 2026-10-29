"""problems: topic

Revision ID: 0011
Revises: 0010
Create Date: 2026-10-12
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: Union[str, None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("problems", sa.Column("topic_slug", sa.String(length=60), nullable=True))
    op.create_index("ix_problems_topic_slug", "problems", ["topic_slug"])


def downgrade() -> None:
    op.drop_index("ix_problems_topic_slug", table_name="problems")
    op.drop_column("problems", "topic_slug")
