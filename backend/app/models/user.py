import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, LargeBinary, String, UniqueConstraint, Uuid
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UTCDateTime


class Role(str, enum.Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"
    moderator = "moderator"


class UserStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    deactivated = "deactivated"


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('student','instructor','admin','moderator')", name="role"),
        CheckConstraint("status IN ('active','suspended','deactivated')", name="status"),
        UniqueConstraint("external_auth_provider", "external_auth_id", name="external_identity"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    external_auth_provider: Mapped[str | None] = mapped_column(String(30))
    external_auth_id: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        String(20), default=Role.student.value, server_default=Role.student.value, index=True, nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default=UserStatus.active.value, server_default=UserStatus.active.value, nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    # Updated (about once a minute) while the person is using the site. Drives "Online" and "Last seen".
    last_seen_at: Mapped[datetime | None] = mapped_column(UTCDateTime)

    profile: Mapped["Profile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )


class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(60), nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    avatar_data: Mapped[bytes | None] = mapped_column(LargeBinary().with_variant(mysql.MEDIUMBLOB(), "mysql"))
    avatar_type: Mapped[str | None] = mapped_column(String(20))
    bio: Mapped[str | None] = mapped_column(String(500))
    github_url: Mapped[str | None] = mapped_column(String(300))
    linkedin_url: Mapped[str | None] = mapped_column(String(300))
    website_url: Mapped[str | None] = mapped_column(String(300))
    location: Mapped[str | None] = mapped_column(String(100))

    user: Mapped[User] = relationship(back_populates="profile")
