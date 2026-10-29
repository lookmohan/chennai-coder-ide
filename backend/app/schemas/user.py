import uuid
from datetime import datetime
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    display_name: str
    avatar_url: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None
    location: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    role: str
    status: str
    created_at: datetime
    last_login_at: datetime | None = None
    profile: ProfileOut


class PublicProfileOut(ProfileOut):
    """Public view: no email, role or account status."""

    joined_at: datetime


def _clean_url(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or len(value) > 300:
        raise ValueError("Must be a valid http(s) URL (max 300 characters)")
    return value


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=60)
    bio: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=100)
    github_url: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None

    @field_validator("github_url", "linkedin_url", "website_url")
    @classmethod
    def _urls(cls, v: str | None) -> str | None:
        return _clean_url(v)

    @field_validator("display_name")
    @classmethod
    def _name(cls, v: str | None) -> str:
        # display_name is NOT NULL in the database: it may be omitted, never nulled or blanked.
        if v is None:
            raise ValueError("Display name cannot be empty")
        v = v.strip()
        if not v:
            raise ValueError("Display name cannot be empty")
        return v


class StudentRow(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    display_name: str
    status: str
    created_at: datetime
    last_login_at: datetime | None = None
