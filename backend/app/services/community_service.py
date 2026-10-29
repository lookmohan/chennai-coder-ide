import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import DiscussionPost, PostReport, Problem, Profile, Role, User
from app.schemas.community import PostOut, ReportOut, ThreadOut
from app.services import audit_service

PAGE_SIZE = 20
STAFF_ROLES = {Role.moderator.value, Role.instructor.value, Role.admin.value}


def is_staff(user: User) -> bool:
    return user.role in STAFF_ROLES


def _post_out(post: DiscussionPost, profile: Profile, viewer: User) -> PostOut:
    author = post.user_id == viewer.id
    return PostOut(
        id=post.id,
        parent_id=post.parent_id,
        author_username=profile.username,
        author_name=profile.display_name,
        body=None if post.is_removed else post.body,
        is_removed=post.is_removed,
        created_at=post.created_at,
        can_delete=(author or is_staff(viewer)) and not post.is_removed,
        can_report=not author and not post.is_removed,
    )


def list_threads(db: Session, problem: Problem, viewer: User, page: int) -> list[ThreadOut]:
    tops = db.execute(
        select(DiscussionPost, Profile)
        .join(Profile, Profile.user_id == DiscussionPost.user_id)
        .where(DiscussionPost.problem_id == problem.id, DiscussionPost.parent_id.is_(None))
        .order_by(DiscussionPost.created_at.desc(), DiscussionPost.id)
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
    ).all()
    if not tops:
        return []

    top_ids = [post.id for post, _ in tops]
    replies = db.execute(
        select(DiscussionPost, Profile)
        .join(Profile, Profile.user_id == DiscussionPost.user_id)
        .where(DiscussionPost.parent_id.in_(top_ids))
        .order_by(DiscussionPost.created_at, DiscussionPost.id)
    ).all()

    by_parent: dict[uuid.UUID, list[PostOut]] = {}
    for reply, profile in replies:
        by_parent.setdefault(reply.parent_id, []).append(_post_out(reply, profile, viewer))

    return [
        ThreadOut(post=_post_out(post, profile, viewer), replies=by_parent.get(post.id, []))
        for post, profile in tops
    ]


def create_post(
    db: Session,
    user: User,
    problem: Problem,
    *,
    body: str,
    parent_id: uuid.UUID | None,
    ip: str | None,
) -> DiscussionPost:
    if parent_id is not None:
        parent = db.get(DiscussionPost, parent_id)
        if parent is None or parent.problem_id != problem.id or parent.is_removed:
            raise AppError("POST_NOT_FOUND", "That post is no longer available.", 404)
        if parent.parent_id is not None:
            raise AppError("REPLY_TO_REPLY", "Reply to the question itself, so threads stay easy to follow.", 400)

    post = DiscussionPost(problem_id=problem.id, user_id=user.id, parent_id=parent_id, body=body)
    db.add(post)
    db.flush()
    # The audit entry records that a post happened, never its text.
    audit_service.record(
        db,
        "discussion.create",
        actor_id=user.id,
        entity_type="discussion_post",
        entity_id=str(post.id),
        metadata={"problem_slug": problem.slug, "reply": parent_id is not None},
        ip=ip,
    )
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: uuid.UUID) -> DiscussionPost:
    post = db.get(DiscussionPost, post_id)
    if post is None:
        raise AppError("POST_NOT_FOUND", "That post doesn't exist.", 404)
    return post


def author_profile(db: Session, post: DiscussionPost) -> Profile:
    return db.scalar(select(Profile).where(Profile.user_id == post.user_id))


def remove_post(db: Session, actor: User, post: DiscussionPost, *, ip: str | None) -> DiscussionPost:
    if post.user_id != actor.id and not is_staff(actor):
        raise AppError("FORBIDDEN", "You can only delete your own posts.", 403)
    if post.is_removed:
        return post
    post.is_removed = True
    post.removed_at = datetime.now(timezone.utc)
    post.body = ""  # the text is gone for good, not just hidden
    audit_service.record(
        db,
        "discussion.remove",
        actor_id=actor.id,
        entity_type="discussion_post",
        entity_id=str(post.id),
        metadata={"by_author": post.user_id == actor.id},
        ip=ip,
    )
    db.commit()
    db.refresh(post)
    return post


def report_post(db: Session, user: User, post: DiscussionPost, reason: str, *, ip: str | None) -> PostReport:
    if post.is_removed:
        raise AppError("POST_NOT_FOUND", "That post is no longer available.", 404)
    if post.user_id == user.id:
        raise AppError("CANNOT_REPORT_OWN", "You can't report your own post.", 400)
    existing = db.scalar(
        select(PostReport.id).where(
            PostReport.post_id == post.id,
            PostReport.reporter_id == user.id,
            PostReport.status == "open",
        )
    )
    if existing is not None:
        raise AppError("ALREADY_REPORTED", "You've already reported this post.", 409)

    report = PostReport(post_id=post.id, reporter_id=user.id, reason=reason)
    db.add(report)
    db.flush()
    audit_service.record(
        db,
        "discussion.report",
        actor_id=user.id,
        entity_type="discussion_post",
        entity_id=str(post.id),
        metadata={"report_id": str(report.id)},
        ip=ip,
    )
    db.commit()
    db.refresh(report)
    return report


def list_reports(db: Session, status: str) -> list[ReportOut]:
    rows = db.execute(
        select(PostReport, DiscussionPost, Profile)
        .join(DiscussionPost, DiscussionPost.id == PostReport.post_id)
        .join(Profile, Profile.user_id == DiscussionPost.user_id)
        .where(PostReport.status == status)
        .order_by(PostReport.created_at)
    ).all()
    reporter_names = {}
    out = []
    for report, post, author in rows:
        if report.reporter_id not in reporter_names:
            reporter = db.scalar(select(Profile).where(Profile.user_id == report.reporter_id))
            reporter_names[report.reporter_id] = reporter.username if reporter else "unknown"
        out.append(
            ReportOut(
                id=report.id,
                post_id=post.id,
                post_body=None if post.is_removed else post.body,
                post_author=author.username,
                reporter_username=reporter_names[report.reporter_id],
                reason=report.reason,
                status=report.status,
                created_at=report.created_at,
            )
        )
    return out


def resolve_report(db: Session, actor: User, report: PostReport, action: str, *, ip: str | None) -> PostReport:
    if report.status != "open":
        raise AppError("ALREADY_RESOLVED", "This report has already been handled.", 409)
    post = db.get(DiscussionPost, report.post_id)
    if action == "remove" and post is not None and not post.is_removed:
        post.is_removed = True
        post.removed_at = datetime.now(timezone.utc)
        post.body = ""
    report.status = "actioned" if action == "remove" else "dismissed"
    report.resolved_at = datetime.now(timezone.utc)
    report.resolved_by = actor.id
    audit_service.record(
        db,
        "report.resolve",
        actor_id=actor.id,
        entity_type="post_report",
        entity_id=str(report.id),
        metadata={"action": action},
        ip=ip,
    )
    db.commit()
    db.refresh(report)
    return report


def get_report(db: Session, report_id: uuid.UUID) -> PostReport:
    report = db.get(PostReport, report_id)
    if report is None:
        raise AppError("REPORT_NOT_FOUND", "That report doesn't exist.", 404)
    return report
