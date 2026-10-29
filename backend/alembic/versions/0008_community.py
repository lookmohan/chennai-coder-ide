"""community: problem discussion threads and reports

Revision ID: 0008
Revises: 0007
Create Date: 2026-10-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_now = sa.func.current_timestamp()
_mysql = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_unicode_ci")


def upgrade() -> None:
    op.create_table(
        "discussion_posts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("problem_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("parent_id", sa.Uuid(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_removed", sa.Boolean(), nullable=False),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], name="fk_discussion_posts_problem_id_problems", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_discussion_posts_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["discussion_posts.id"], name="fk_discussion_posts_parent_id_discussion_posts", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_discussion_posts"),
        **_mysql,
    )
    op.create_index("ix_discussion_posts_problem_id", "discussion_posts", ["problem_id"])
    op.create_index("ix_discussion_posts_user_id", "discussion_posts", ["user_id"])
    op.create_index("ix_discussion_posts_parent_id", "discussion_posts", ["parent_id"])

    op.create_table(
        "post_reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("post_id", sa.Uuid(), nullable=False),
        sa.Column("reporter_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.String(length=300), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="open", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_by", sa.Uuid(), nullable=True),
        sa.CheckConstraint("status IN ('open','dismissed','actioned')", name="ck_post_reports_status"),
        sa.ForeignKeyConstraint(["post_id"], ["discussion_posts.id"], name="fk_post_reports_post_id_discussion_posts", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], name="fk_post_reports_reporter_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["resolved_by"], ["users.id"], name="fk_post_reports_resolved_by_users", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name="pk_post_reports"),
        **_mysql,
    )
    op.create_index("ix_post_reports_post_id", "post_reports", ["post_id"])
    op.create_index("ix_post_reports_reporter_id", "post_reports", ["reporter_id"])
    op.create_index("ix_post_reports_status", "post_reports", ["status"])


def downgrade() -> None:
    op.drop_table("post_reports")
    op.drop_table("discussion_posts")
