from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.content.topics import LEVEL_TARGETS, TOPICS
from app.core.errors import AppError
from app.models import Problem
from app.services.problem_service import to_list_item

LEVELS = ("Easy", "Medium", "Hard")


def _empty_counts() -> dict[str, int]:
    return {level: 0 for level in LEVELS}


def summaries(db: Session) -> list[dict]:
    """Every topic in learning order, with published question counts per level against the targets."""
    rows = db.execute(
        select(Problem.topic_slug, Problem.difficulty, func.count(Problem.id))
        .where(Problem.status == "published")
        .group_by(Problem.topic_slug, Problem.difficulty)
    ).all()
    counts: dict[str, dict[str, int]] = {}
    for slug, level, total in rows:
        counts.setdefault(slug, _empty_counts())[level] = total

    return [
        {
            **topic,
            "number": number,
            "counts": counts.get(topic["slug"], _empty_counts()),
            "targets": LEVEL_TARGETS,
        }
        for number, topic in enumerate(TOPICS, start=1)
    ]


def get_topic(slug: str) -> dict:
    for number, topic in enumerate(TOPICS, start=1):
        if topic["slug"] == slug:
            return {**topic, "number": number, "targets": LEVEL_TARGETS}
    raise AppError("TOPIC_NOT_FOUND", "That topic doesn't exist.", 404)


def topic_problems(db: Session, slug: str) -> dict[str, list[dict]]:
    """Published problems for one topic, grouped by level, in learning order."""
    rows = db.scalars(
        select(Problem)
        .where(Problem.status == "published", Problem.topic_slug == slug)
        .order_by(Problem.sort_order, Problem.title)
    ).all()
    grouped: dict[str, list[dict]] = {level: [] for level in LEVELS}
    for problem in rows:
        grouped[problem.difficulty].append(to_list_item(problem).model_dump())
    return grouped
