"""coding engine: problems, problem_test_cases, submissions

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-08
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_now = sa.func.current_timestamp()
_mysql = dict(mysql_charset="utf8mb4", mysql_collate="utf8mb4_unicode_ci")

_SUBMISSION_STATUSES = (
    "QUEUED", "RUNNING", "ACCEPTED", "WRONG_ANSWER", "COMPILATION_ERROR",
    "RUNTIME_ERROR", "TIME_LIMIT_EXCEEDED", "MEMORY_LIMIT_EXCEEDED", "SYSTEM_ERROR",
)


def upgrade() -> None:
    op.create_table(
        "problems",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="draft", nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("input_format", sa.Text(), nullable=True),
        sa.Column("output_format", sa.Text(), nullable=True),
        sa.Column("constraints", sa.Text(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("time_limit_ms", sa.Integer(), nullable=False),
        sa.Column("memory_limit_mb", sa.Integer(), nullable=False),
        sa.Column("starter_code", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.CheckConstraint("difficulty IN ('Easy','Medium','Hard')", name="ck_problems_difficulty"),
        sa.CheckConstraint("status IN ('draft','published','archived')", name="ck_problems_status"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], name="fk_problems_created_by_users", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name="pk_problems"),
        **_mysql,
    )
    op.create_index("ix_problems_slug", "problems", ["slug"], unique=True)
    op.create_index("ix_problems_difficulty", "problems", ["difficulty"])
    op.create_index("ix_problems_status", "problems", ["status"])

    op.create_table(
        "problem_test_cases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("problem_id", sa.Uuid(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("stdin", sa.Text(), nullable=False),
        sa.Column("expected_output", sa.Text(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["problem_id"], ["problems.id"], name="fk_problem_test_cases_problem_id_problems", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_problem_test_cases"),
        **_mysql,
    )
    op.create_index("ix_problem_test_cases_problem_id", "problem_test_cases", ["problem_id"])
    op.create_index(
        "ix_problem_test_cases_problem_position", "problem_test_cases", ["problem_id", "position"], unique=True
    )

    op.create_table(
        "submissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("problem_id", sa.Uuid(), nullable=False),
        sa.Column("language", sa.String(length=20), nullable=False),
        sa.Column("source_code", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="QUEUED", nullable=False),
        sa.Column("passed_count", sa.Integer(), nullable=False),
        sa.Column("total_count", sa.Integer(), nullable=False),
        sa.Column("failed_test_position", sa.Integer(), nullable=True),
        sa.Column("runtime_ms", sa.Integer(), nullable=True),
        sa.Column("memory_kb", sa.Integer(), nullable=True),
        sa.Column("message", sa.String(length=500), nullable=True),
        sa.Column("judged_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=_now, nullable=False),
        sa.CheckConstraint(
            "status IN (" + ", ".join(f"'{s}'" for s in _SUBMISSION_STATUSES) + ")", name="ck_submissions_status"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_submissions_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["problem_id"], ["problems.id"], name="fk_submissions_problem_id_problems", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_submissions"),
        **_mysql,
    )
    op.create_index("ix_submissions_user_id", "submissions", ["user_id"])
    op.create_index("ix_submissions_problem_id", "submissions", ["problem_id"])


def downgrade() -> None:
    op.drop_table("submissions")
    op.drop_table("problem_test_cases")
    op.drop_table("problems")
