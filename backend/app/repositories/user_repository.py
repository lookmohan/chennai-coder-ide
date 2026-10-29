import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Profile, Role, User


def get_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).join(Profile).where(Profile.username == username))


def list_students(
    db: Session, *, page: int, page_size: int, query: str | None = None
) -> tuple[list[tuple[User, Profile]], int]:
    conditions = [User.role == Role.student.value]
    if query and query.strip():
        pattern = f"%{query.strip()}%"
        conditions.append(
            or_(
                Profile.username.ilike(pattern),
                Profile.display_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    total = (
        db.scalar(
            select(func.count(User.id))
            .select_from(User)
            .join(Profile, Profile.user_id == User.id)
            .where(*conditions)
        )
        or 0
    )
    rows = db.execute(
        select(User, Profile)
        .join(Profile, Profile.user_id == User.id)
        .where(*conditions)
        .order_by(User.created_at.desc(), User.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return [(u, p) for u, p in rows], total
