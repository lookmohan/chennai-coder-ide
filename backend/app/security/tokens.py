import secrets
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings
from app.core.errors import AppError

ALGORITHM = "HS256"


def create_access_token(user_id: uuid.UUID) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expires_minutes),
        "jti": secrets.token_hex(8),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            get_settings().jwt_secret,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        return uuid.UUID(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise AppError("TOKEN_EXPIRED", "Your session has expired. Please log in again.", 401)
    except (jwt.InvalidTokenError, ValueError):
        raise AppError("INVALID_TOKEN", "Invalid authentication token.", 401)


def new_csrf_token() -> str:
    return secrets.token_urlsafe(32)
