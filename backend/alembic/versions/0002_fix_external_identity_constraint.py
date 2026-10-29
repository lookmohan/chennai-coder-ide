"""fix unique constraint name on users.external_identity

MySQL auto-prefixed the constraint name with the table name when creating it
through Alembic, producing uq_users_uq_users_external_identity instead of
uq_users_external_identity. This migration drops the old index and re-creates
it with the correct name so `alembic check` stays clean.

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-07
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the double-prefixed index MySQL created automatically.
    op.drop_index(
        "uq_users_uq_users_external_identity",
        table_name="users",
    )
    # Re-create it with the name Alembic expects.
    op.create_unique_constraint(
        "uq_users_external_identity",
        "users",
        ["external_auth_provider", "external_auth_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_users_external_identity", "users", type_="unique")
    op.create_index(
        "uq_users_uq_users_external_identity",
        "users",
        ["external_auth_provider", "external_auth_id"],
        unique=True,
    )
