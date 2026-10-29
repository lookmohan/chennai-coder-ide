import re
import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
Difficulty = Literal["Easy", "Medium", "Hard"]
ProblemStatus = Literal["draft", "published", "archived"]


class TestCaseIn(BaseModel):
    stdin: str = Field(default="", max_length=10000)
    expected_output: str = Field(max_length=10000)
    is_hidden: bool = True
    explanation: str | None = Field(default=None, max_length=2000)


class ProblemIn(BaseModel):
    slug: str = Field(min_length=3, max_length=120)
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=10000)
    difficulty: Difficulty
    status: ProblemStatus = "draft"
    sort_order: int = Field(default=0, ge=0, le=100000)
    tags: list[str] = Field(default_factory=list, max_length=10)
    input_format: str | None = Field(default=None, max_length=3000)
    output_format: str | None = Field(default=None, max_length=3000)
    constraints: str | None = Field(default=None, max_length=3000)
    explanation: str | None = Field(default=None, max_length=3000)
    time_limit_ms: int = Field(default=2000, ge=100, le=10000)
    memory_limit_mb: int = Field(default=256, ge=16, le=1024)
    starter_code: dict[str, str] = Field(default_factory=lambda: {"python": "# Write your solution here\n"})
    tests: list[TestCaseIn] = Field(min_length=1, max_length=50)

    @field_validator("slug")
    @classmethod
    def _slug(cls, value: str) -> str:
        value = value.strip().lower()
        if not SLUG_RE.match(value):
            raise ValueError("Use lower-case letters, numbers and single hyphens only, for example double-it")
        return value

    @field_validator("tags")
    @classmethod
    def _tags(cls, value: list[str]) -> list[str]:
        return [tag.strip()[:30] for tag in value if tag.strip()]

    @field_validator("starter_code")
    @classmethod
    def _starter(cls, value: dict[str, str]) -> dict[str, str]:
        if set(value) != {"python"}:
            raise ValueError("Starter code must be given for Python only")
        return value


class TestCaseOut(BaseModel):
    position: int
    stdin: str
    expected_output: str
    is_hidden: bool
    explanation: str | None = None


class ProblemAdminOut(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    difficulty: str
    status: str
    sort_order: int
    tags: list[str]
    input_format: str | None = None
    output_format: str | None = None
    constraints: str | None = None
    explanation: str | None = None
    time_limit_ms: int
    memory_limit_mb: int
    starter_code: dict[str, str]
    tests: list[TestCaseOut]
    updated_at: datetime


class ProblemRowOut(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    difficulty: str
    status: str
    sort_order: int
    test_count: int
    visible_count: int
    updated_at: datetime


class StatusIn(BaseModel):
    status: ProblemStatus


class OverviewOut(BaseModel):
    students: int
    active_students_7d: int
    problems_published: int
    problems_draft: int
    problems_archived: int


class AuditOut(BaseModel):
    id: uuid.UUID
    action: str
    entity_type: str | None = None
    entity_id: str | None = None
    actor_id: uuid.UUID | None = None
    metadata: dict[str, Any] = {}
    ip: str | None = None
    created_at: datetime
