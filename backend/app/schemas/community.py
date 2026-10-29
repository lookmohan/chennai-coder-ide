import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PostCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)
    parent_id: uuid.UUID | None = None

    @field_validator("body")
    @classmethod
    def _body(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Write something before posting.")
        return value


class PostOut(BaseModel):
    id: uuid.UUID
    parent_id: uuid.UUID | None = None
    author_username: str
    author_name: str
    body: str | None
    is_removed: bool
    created_at: datetime
    can_delete: bool
    can_report: bool


class ThreadOut(BaseModel):
    post: PostOut
    replies: list[PostOut]


class ReportCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=300)


class ReportOut(BaseModel):
    id: uuid.UUID
    post_id: uuid.UUID
    post_body: str | None
    post_author: str
    reporter_username: str
    reason: str
    status: str
    created_at: datetime


class ResolveIn(BaseModel):
    action: Literal["dismiss", "remove"]
