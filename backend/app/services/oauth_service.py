import re
import secrets
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import Profile, Role, User, UserStatus
from app.repositories import user_repository as users
from app.security.oauth import OAuthProfile
from app.services import audit_service


def _unique_username(db: Session, hint: str) -> str:
    base = re.sub(r"[^a-z0-9_]", "_", (hint or "").lower()).strip("_")[:24]
    if len(base) < 3:
        base = (base + "learner")[:24]
    candidate = base
    while users.get_by_username(db, candidate) is not None:
        candidate = f"{base[:20]}_{secrets.randbelow(10000):04d}"
    return candidate


def sign_in_with_provider(db: Session, profile: OAuthProfile, *, ip: str | None) -> User:
    user = db.scalar(
        select(User).where(
            User.external_auth_provider == profile.provider,
            User.external_auth_id == profile.external_id,
        )
    )

    if user is None:
        existing = users.get_by_email(db, profile.email)
        if existing is not None:
            # Only link to an existing account when the provider has verified the email.
            if not profile.email_verified:
                raise AppError(
                    "EMAIL_IN_USE",
                    "An account with this email already exists. Log in with your password instead.",
                    409,
                )
            if existing.external_auth_provider and existing.external_auth_provider != profile.provider:
                raise AppError(
                    "EMAIL_IN_USE",
                    "This email is already linked to a different sign-in method.",
                    409,
                )
            existing.external_auth_provider = profile.provider
            existing.external_auth_id = profile.external_id
            user = existing
        else:
            user = User(
                email=profile.email,
                password_hash=None,  # sign-in through the provider only
                external_auth_provider=profile.provider,
                external_auth_id=profile.external_id,
                role=Role.student.value,
                status=UserStatus.active.value,
            )
            user.profile = Profile(
                display_name=(profile.display_name or "Learner")[:60],
                username=_unique_username(db, profile.username_hint),
            )
            db.add(user)

    if user.status != UserStatus.active.value:
        raise AppError("ACCOUNT_SUSPENDED", "This account is not active. Contact support.", 403)

    user.last_login_at = datetime.now(timezone.utc)
    audit_service.record(
        db,
        "auth.oauth_login",
        actor_id=user.id,
        entity_type="user",
        entity_id=str(user.id),
        metadata={"provider": profile.provider},
        ip=ip,
    )
    db.commit()
    db.refresh(user)
    return user
