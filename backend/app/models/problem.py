import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UTCDateTime


class Difficulty(str, enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class ProblemStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class SubmissionStatus(str, enum.Enum):
    queued = "QUEUED"
    running = "RUNNING"
    accepted = "ACCEPTED"
    wrong_answer = "WRONG_ANSWER"
    compilation_error = "COMPILATION_ERROR"
    runtime_error = "RUNTIME_ERROR"
    time_limit_exceeded = "TIME_LIMIT_EXCEEDED"
    memory_limit_exceeded = "MEMORY_LIMIT_EXCEEDED"
    system_error = "SYSTEM_ERROR"


_SUBMISSION_STATUS_SQL = ", ".join(f"'{s.value}'" for s in SubmissionStatus)


class Problem(TimestampMixin, Base):
    __tablename__ = "problems"
    __table_args__ = (
        CheckConstraint("difficulty IN ('Easy','Medium','Hard')", name="difficulty"),
        CheckConstraint("status IN ('draft','published','archived')", name="status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=ProblemStatus.draft.value, server_default=ProblemStatus.draft.value, index=True, nullable=False
    )
    # Which Python concept this problem belongs to, for example "lists" (see app/content/topics.py).
    topic_slug: Mapped[str | None] = mapped_column(String(60), index=True)
    # Position in the learning path: 1 is the first problem a student sees.
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", index=True, nullable=False)
    tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    input_format: Mapped[str | None] = mapped_column(Text)
    output_format: Mapped[str | None] = mapped_column(Text)
    constraints: Mapped[str | None] = mapped_column(Text)
    explanation: Mapped[str | None] = mapped_column(Text)
    time_limit_ms: Mapped[int] = mapped_column(Integer, default=2000, nullable=False)
    memory_limit_mb: Mapped[int] = mapped_column(Integer, default=256, nullable=False)
    # {"python": "...", "javascript": "..."}; only languages listed here are offered.
    starter_code: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id", ondelete="SET NULL"))

    test_cases: Mapped[list["ProblemTestCase"]] = relationship(
        back_populates="problem",
        cascade="all, delete-orphan",
        order_by="ProblemTestCase.position",
    )


class ProblemTestCase(Base):
    """Hidden tests (is_hidden=True) must never be returned by any public schema."""

    __tablename__ = "problem_test_cases"
    __table_args__ = (Index("ix_problem_test_cases_problem_position", "problem_id", "position", unique=True),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("problems.id", ondelete="CASCADE"), index=True, nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    stdin: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # Shown under visible examples only: why the output is what it is.
    explanation: Mapped[str | None] = mapped_column(Text)

    problem: Mapped[Problem] = relationship(back_populates="test_cases")


class Submission(TimestampMixin, Base):
    __tablename__ = "submissions"
    __table_args__ = (CheckConstraint(f"status IN ({_SUBMISSION_STATUS_SQL})", name="status"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    problem_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("problems.id", ondelete="CASCADE"), index=True, nullable=False
    )
    language: Mapped[str] = mapped_column(String(20), nullable=False)
    source_code: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default=SubmissionStatus.queued.value, server_default=SubmissionStatus.queued.value, nullable=False
    )
    passed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_test_position: Mapped[int | None] = mapped_column(Integer)
    runtime_ms: Mapped[int | None] = mapped_column(Integer)
    memory_kb: Mapped[int | None] = mapped_column(Integer)
    message: Mapped[str | None] = mapped_column(String(500))
    judged_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
