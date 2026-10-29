from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.rate_limit import client_ip, enforce_rate_limit
from app.models import User
from app.schemas.common import Envelope
from app.services import chat_service as svc

router = APIRouter(prefix="/chat", tags=["chat"])


class MessageIn(BaseModel):
    body: str = Field(min_length=1, max_length=500)

    @field_validator("body")
    @classmethod
    def _body(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Write a message before sending.")
        return value


@router.get("/room", response_model=Envelope[list[dict]])
def read_room(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Envelope[list[dict]]:
    return Envelope(data=svc.room_messages(db, user))


@router.post("/room", status_code=201, response_model=Envelope[dict])
def post_to_room(
    payload: MessageIn,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[dict]:
    # Enough for a conversation; not enough to flood the room.
    enforce_rate_limit(f"room:{user.id}", 20, 60)
    message = svc.send_to_room(db, user, payload.body, ip=client_ip(request))
    return Envelope(
        data={
            "id": str(message.id),
            "body": message.body,
            "created_at": message.created_at.isoformat(),
            "author_username": user.profile.username,
            "author_name": user.profile.display_name,
            "mine": True,
            "can_delete": True,
        }
    )


@router.delete("/room/{message_id}", response_model=Envelope[dict])
def delete_from_room(
    message_id: str,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[dict]:
    import uuid as _uuid

    try:
        parsed = _uuid.UUID(message_id)
    except ValueError:
        from app.core.errors import AppError

        raise AppError("MESSAGE_NOT_FOUND", "That message doesn't exist.", 404)
    svc.delete_from_room(db, user, parsed, ip=client_ip(request))
    return Envelope(data={"deleted": True})


@router.get("/people", response_model=Envelope[list[dict]])
def find_people(
    q: str | None = Query(None, max_length=60),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[list[dict]]:
    return Envelope(data=svc.people(db, user, q))
