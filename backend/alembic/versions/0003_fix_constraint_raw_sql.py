"""fix unique constraint name on users.external_identity (raw SQL)

MySQL keeps unique constraints as indexes. The previous migration used
op.drop_index which didn't remove it. This one uses raw ALTER TABLE
statements which work regardless of whether MySQL treats it as a
constraint or an index.

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-07
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE users DROP INDEX `uq_users_uq_users_external_identity`")
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT `uq_users_external_identity` "
        "UNIQUE (`external_auth_provider`, `external_auth_id`)"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE users DROP INDEX `uq_users_external_identity`")
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT `uq_users_uq_users_external_identity` "
        "UNIQUE (`external_auth_provider`, `external_auth_id`)"
    )
