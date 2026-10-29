from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import DiscussionPost, Problem, Profile, User
from app.services.community_service import _post_out


def latest_threads(db: Session, viewer: User, page: int, page_size: int = 20) -> list[dict]:
    """Newest questions across all published problems, with their problem and reply count."""
    rows = db.execute(
        select(DiscussionPost, Profile, Problem)
        .join(Profile, Profile.user_id == DiscussionPost.user_id)
        .join(Problem, Problem.id == DiscussionPost.problem_id)
        .where(DiscussionPost.parent_id.is_(None), Problem.status == "published")
        .order_by(DiscussionPost.created_at.desc(), DiscussionPost.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    if not rows:
        return []

    post_ids = [post.id for post, _, _ in rows]
    counts = dict(
        db.execute(
            select(DiscussionPost.parent_id, func.count(DiscussionPost.id))
            .where(DiscussionPost.parent_id.in_(post_ids))
            .group_by(DiscussionPost.parent_id)
        ).all()
    )

    return [
        {
            "post": _post_out(post, profile, viewer),
            "problem_slug": problem.slug,
            "problem_title": problem.title,
            "reply_count": counts.get(post.id, 0),
        }
        for post, profile, problem in rows
    ]
