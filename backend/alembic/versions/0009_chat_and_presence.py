"""chat messages and presence (last seen)

Revision ID: 0009
Revises: 0008
Create Date: 2026-10-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_now = sa.func.current_timestamp()
_mysql = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_unicode_ci")


def upgrade() -> None:
    op.add_column("users", sa.Column("last_seen_at", sa.DateTime(), nullable=True))

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("sender_id", sa.Uuid(), nullable=False),
        sa.Column("recipient_id", sa.Uuid(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.Column("read_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], name="fk_chat_messages_sender_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["recipient_id"], ["users.id"], name="fk_chat_messages_recipient_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_chat_messages"),
        **_mysql,
    )
    op.create_index("ix_chat_messages_pair", "chat_messages", ["sender_id", "recipient_id", "created_at"])
    op.create_index("ix_chat_messages_recipient_unread", "chat_messages", ["recipient_id", "read_at"])


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_column("users", "last_seen_at")
