import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Problem


def get_published_by_slug(db: Session, slug: str) -> Problem | None:
    return db.scalar(select(Problem).where(Problem.slug == slug, Problem.status == "published"))


def get_by_id(db: Session, problem_id: uuid.UUID) -> Problem | None:
    return db.get(Problem, problem_id)


def list_published(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    difficulty: str | None = None,
) -> tuple[list[Problem], int]:
    conditions = [Problem.status == "published"]
    if q and q.strip():
        conditions.append(Problem.title.ilike(f"%{q.strip()}%"))
    if difficulty:
        conditions.append(Problem.difficulty == difficulty)

    total = db.scalar(select(func.count(Problem.id)).where(*conditions)) or 0
    rows = db.scalars(
        select(Problem)
        .where(*conditions)
        .order_by(Problem.sort_order, Problem.title, Problem.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return list(rows), total


def list_all(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    status: str | None = None,
) -> tuple[list[Problem], int]:
    """Every problem, including drafts and archived ones. Staff only."""
    conditions = []
    if q and q.strip():
        conditions.append(Problem.title.ilike(f"%{q.strip()}%"))
    if status:
        conditions.append(Problem.status == status)

    total = db.scalar(select(func.count(Problem.id)).where(*conditions)) or 0
    rows = db.scalars(
        select(Problem)
        .where(*conditions)
        .order_by(Problem.sort_order, Problem.title, Problem.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return list(rows), total
