import hmac
from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.models import Role, User, UserStatus
from app.repositories import user_repository as users
from app.security.tokens import decode_access_token

COOKIE_ACCESS = "cc_access"
COOKIE_CSRF = "cc_csrf"
CSRF_HEADER = "x-csrf-token"
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
# "Last seen" is refreshed at most this often, so most requests don't write to the database.
PRESENCE_WRITE_INTERVAL = timedelta(seconds=60)


def _verify_csrf(request: Request) -> None:
    """Double-submit check, required for state-changing requests authenticated by cookie."""
    cookie = request.cookies.get(COOKIE_CSRF, "")
    header = request.headers.get(CSRF_HEADER, "")
    if not cookie or not header or not hmac.compare_digest(cookie, header):
        raise AppError("CSRF_FAILED", "Missing or invalid CSRF token.", 403)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    authorization = request.headers.get("authorization", "")
    if authorization.lower().startswith("bearer "):
        token, via_cookie = authorization[7:].strip(), False
    else:
        token, via_cookie = request.cookies.get(COOKIE_ACCESS), True

    if not token:
        raise AppError("NOT_AUTHENTICATED", "Authentication required.", 401)
    if via_cookie and request.method not in SAFE_METHODS:
        _verify_csrf(request)

    user = users.get_by_id(db, decode_access_token(token))
    if user is None:
        raise AppError("NOT_AUTHENTICATED", "Authentication required.", 401)
    if user.status != UserStatus.active.value:
        raise AppError("ACCOUNT_SUSPENDED", "This account is not active.", 403)

    # Presence: note that this person is here. Written at most once a minute.
    now = datetime.now(timezone.utc)
    if user.last_seen_at is None or now - user.last_seen_at >= PRESENCE_WRITE_INTERVAL:
        user.last_seen_at = now
        db.commit()
    return user


def require_roles(*roles: Role):
    """Role is read from the database on every request, never from the token."""
    allowed = {r.value for r in roles}

    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise AppError("FORBIDDEN", "You do not have permission to perform this action.", 403)
        return user

    return dependency
