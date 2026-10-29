import uuid

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import ChatRoomMessage, Profile, User, UserStatus
from app.services import audit_service
from app.services.community_service import is_staff
from app.services.presence import presence

ROOM_LIMIT = 100


def _person(user: User) -> dict:
    return {
        "username": user.profile.username,
        "display_name": user.profile.display_name,
        "avatar_url": user.profile.avatar_url,
        "presence": presence(user.last_seen_at),
    }


def room_messages(db: Session, viewer: User) -> list[dict]:
    rows = db.execute(
        select(ChatRoomMessage, Profile)
        .join(Profile, Profile.user_id == ChatRoomMessage.author_id)
        .order_by(ChatRoomMessage.created_at.desc(), ChatRoomMessage.id)
        .limit(ROOM_LIMIT)
    ).all()
    rows.reverse()
    staff = is_staff(viewer)
    return [
        {
            "id": str(message.id),
            "body": message.body,
            "created_at": message.created_at.isoformat(),
            "author_username": profile.username,
            "author_name": profile.display_name,
            "mine": message.author_id == viewer.id,
            "can_delete": message.author_id == viewer.id or staff,
        }
        for message, profile in rows
    ]


def send_to_room(db: Session, viewer: User, body: str, *, ip: str | None) -> ChatRoomMessage:
    message = ChatRoomMessage(author_id=viewer.id, body=body)
    db.add(message)
    db.flush()
    # The audit entry records that a message was sent, never its text.
    audit_service.record(
        db,
        "chat.room_send",
        actor_id=viewer.id,
        entity_type="chat_room_message",
        entity_id=str(message.id),
        metadata={},
        ip=ip,
    )
    db.commit()
    db.refresh(message)
    return message


def delete_from_room(db: Session, actor: User, message_id: uuid.UUID, *, ip: str | None) -> None:
    message = db.get(ChatRoomMessage, message_id)
    if message is None:
        raise AppError("MESSAGE_NOT_FOUND", "That message doesn't exist.", 404)
    if message.author_id != actor.id and not is_staff(actor):
        raise AppError("FORBIDDEN", "You can only delete your own messages.", 403)
    audit_service.record(
        db,
        "chat.room_delete",
        actor_id=actor.id,
        entity_type="chat_room_message",
        entity_id=str(message.id),
        metadata={"by_author": message.author_id == actor.id},
        ip=ip,
    )
    db.delete(message)
    db.commit()


def people(db: Session, viewer: User, q: str | None) -> list[dict]:
    """Everyone else, most recently active first, with online / last-seen wording. You are not listed."""
    stmt = (
        select(User)
        .join(Profile, Profile.user_id == User.id)
        .where(User.id != viewer.id, User.status == UserStatus.active.value)
    )
    if q and q.strip():
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(Profile.username.ilike(pattern), Profile.display_name.ilike(pattern)))
    users = db.scalars(stmt.order_by(User.last_seen_at.desc(), Profile.username).limit(50)).all()
    return [_person(u) for u in users]
