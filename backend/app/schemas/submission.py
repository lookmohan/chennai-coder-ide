import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
    problem_slug: str = Field(min_length=1, max_length=120)
    language: str = Field(min_length=1, max_length=20)
    source_code: str = Field(min_length=1, max_length=65536)


class SubmissionOut(BaseModel):
    id: uuid.UUID
    problem_slug: str
    language: str
    source_code: str
    status: str
    passed_count: int
    total_count: int
    failed_test_position: int | None = None
    runtime_ms: int | None = None
    memory_kb: int | None = None
    message: str | None = None
    created_at: datetime
    judged_at: datetime | None = None
