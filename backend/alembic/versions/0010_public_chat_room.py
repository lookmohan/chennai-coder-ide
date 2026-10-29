"""public community room replaces direct messages

Revision ID: 0010
Revises: 0009
Create Date: 2026-10-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_now = sa.func.current_timestamp()
_mysql = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_unicode_ci")


def upgrade() -> None:
    # Direct messages are not part of the product. The table was created in 0009 and never used.
    # Dropping the table also removes its indexes and foreign keys, which MySQL requires
    # before the indexes can go.
    op.drop_table("chat_messages")

    op.create_table(
        "chat_room_messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("author_id", sa.Uuid(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], name="fk_chat_room_messages_author_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_chat_room_messages"),
        **_mysql,
    )
    op.create_index("ix_chat_room_messages_created_at", "chat_room_messages", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_chat_room_messages_created_at", table_name="chat_room_messages")
    op.drop_table("chat_room_messages")
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
