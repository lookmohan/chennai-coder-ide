"""profile photo columns

Revision ID: 0006
Revises: 0005
Create Date: 2026-10-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profiles",
        sa.Column("avatar_data", sa.LargeBinary().with_variant(mysql.MEDIUMBLOB(), "mysql"), nullable=True),
    )
    op.add_column("profiles", sa.Column("avatar_type", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("profiles", "avatar_type")
    op.drop_column("profiles", "avatar_data")
