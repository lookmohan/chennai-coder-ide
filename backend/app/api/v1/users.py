import hashlib

from fastapi import APIRouter, Depends, File, Response, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.errors import AppError
from app.models import User, UserStatus
from app.repositories import user_repository as users
from app.schemas.common import Envelope
from app.schemas.user import ProfileUpdate, PublicProfileOut, UserOut

router = APIRouter(prefix="/users", tags=["users"])

MAX_AVATAR_BYTES = 512 * 1024


def detect_image_type(data: bytes) -> str | None:
    """Identify the image from its contents, not its file name or the type the browser claims."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if len(data) >= 12 and data[0:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def _avatar_url(username: str, data: bytes) -> str:
    # The hash changes with each new photo, so browsers never show a stale one.
    return f"/api/v1/users/{username}/avatar?v={hashlib.sha256(data).hexdigest()[:12]}"


@router.get("/me", response_model=Envelope[UserOut])
def get_me(user: User = Depends(get_current_user)) -> Envelope[UserOut]:
    return Envelope(data=UserOut.model_validate(user))


@router.patch("/me", response_model=Envelope[UserOut])
def update_me(
    payload: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[UserOut]:
    # exclude_unset: only fields the client actually sent are changed.
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user.profile, field, value)
    db.commit()
    db.refresh(user)
    return Envelope(data=UserOut.model_validate(user))


@router.post("/me/avatar", response_model=Envelope[UserOut])
def upload_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[UserOut]:
    data = file.file.read(MAX_AVATAR_BYTES + 1)
    if len(data) > MAX_AVATAR_BYTES:
        raise AppError("AVATAR_TOO_LARGE", "Please choose an image under 512 KB.", 413)
    kind = detect_image_type(data)
    if kind is None:
        raise AppError("AVATAR_INVALID_TYPE", "Please upload a PNG, JPEG or WebP image.", 415)

    profile = user.profile
    profile.avatar_data = data
    profile.avatar_type = kind
    profile.avatar_url = _avatar_url(profile.username, data)
    db.commit()
    db.refresh(user)
    return Envelope(data=UserOut.model_validate(user))


@router.delete("/me/avatar", response_model=Envelope[UserOut])
def remove_avatar(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Envelope[UserOut]:
    user.profile.avatar_data = None
    user.profile.avatar_type = None
    user.profile.avatar_url = None
    db.commit()
    db.refresh(user)
    return Envelope(data=UserOut.model_validate(user))


@router.get("/{username}/avatar")
def get_avatar(username: str, db: Session = Depends(get_db)) -> Response:
    """Profile photos are public, like the profile itself."""
    user = users.get_by_username(db, username.strip().lower())
    if user is None or user.status != UserStatus.active.value or user.profile.avatar_data is None:
        raise AppError("AVATAR_NOT_FOUND", "No profile photo.", 404)
    return Response(
        content=user.profile.avatar_data,
        media_type=user.profile.avatar_type or "application/octet-stream",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/{username}", response_model=Envelope[PublicProfileOut])
def public_profile(username: str, db: Session = Depends(get_db)) -> Envelope[PublicProfileOut]:
    user = users.get_by_username(db, username.strip().lower())
    if user is None or user.status != UserStatus.active.value:
        raise AppError("USER_NOT_FOUND", "User not found.", 404)
    p = user.profile
    return Envelope(
        data=PublicProfileOut(
            username=p.username,
            display_name=p.display_name,
            avatar_url=p.avatar_url,
            bio=p.bio,
            github_url=p.github_url,
            linkedin_url=p.linkedin_url,
            website_url=p.website_url,
            location=p.location,
            joined_at=user.created_at,
        )
    )
