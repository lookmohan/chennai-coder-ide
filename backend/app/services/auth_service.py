import logging
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.logging import hash_identifier
from app.models import Profile, Role, User, UserStatus
from app.repositories import user_repository as users
from app.security.passwords import burn_verification_time, hash_password, needs_rehash, verify_password
from app.services import audit_service

logger = logging.getLogger("app.auth")


def register_user(
    db: Session,
    *,
    email: str,
    password: str,
    username: str,
    display_name: str,
    role: Role = Role.student,
    ip: str | None = None,
) -> User:
    email = email.strip().lower()
    if users.get_by_email(db, email):
        raise AppError("EMAIL_TAKEN", "An account with this email already exists.", 409)
    if users.get_by_username(db, username):
        raise AppError("USERNAME_TAKEN", "This username is already taken.", 409)

    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role.value,
        status=UserStatus.active.value,
    )
    user.profile = Profile(display_name=display_name, username=username)
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        # Lost a race against a concurrent registration.
        db.rollback()
        raise AppError("ACCOUNT_EXISTS", "An account with these details already exists.", 409)

    audit_service.record(
        db,
        "auth.register",
        actor_id=user.id,
        entity_type="user",
        entity_id=str(user.id),
        metadata={"role": role.value},
        ip=ip,
    )
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, *, email: str, password: str, ip: str | None = None) -> User:
    email = email.strip().lower()
    user = users.get_by_email(db, email)

    if user is None or user.password_hash is None:
        burn_verification_time(password)
        _log_failure(email, "unknown_account_or_no_password", ip)
        raise AppError("INVALID_CREDENTIALS", "Incorrect email or password.", 401)

    if not verify_password(user.password_hash, password):
        _log_failure(email, "bad_password", ip)
        raise AppError("INVALID_CREDENTIALS", "Incorrect email or password.", 401)

    # Status is only revealed after a correct password.
    if user.status != UserStatus.active.value:
        _log_failure(email, f"status_{user.status}", ip)
        raise AppError("ACCOUNT_SUSPENDED", "This account is not active. Contact support.", 403)

    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)
    user.last_login_at = datetime.now(timezone.utc)
    audit_service.record(db, "auth.login", actor_id=user.id, entity_type="user", entity_id=str(user.id), ip=ip)
    db.commit()
    db.refresh(user)
    return user


def _log_failure(email: str, reason: str, ip: str | None) -> None:
    logger.warning(
        "auth.login_failed",
        extra={"email_hash": hash_identifier(email), "reason": reason, "ip": ip},
    )
