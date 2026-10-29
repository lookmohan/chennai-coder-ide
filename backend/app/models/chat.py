import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Index, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UTCDateTime


class ChatRoomMessage(Base):
    """A message in the public community room. Everyone signed in can read it."""

    __tablename__ = "chat_room_messages"
    __table_args__ = (Index("ix_chat_room_messages_created_at", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, server_default=func.current_timestamp(), nullable=False)
