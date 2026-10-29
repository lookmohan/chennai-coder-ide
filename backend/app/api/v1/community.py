import uuid

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.core.errors import AppError
from app.core.rate_limit import client_ip, enforce_rate_limit
from app.models import Role, User
from app.repositories import problem_repository as problems
from app.schemas.common import Envelope
from app.schemas.community import PostCreate, PostOut, ReportCreate, ReportOut, ResolveIn, ThreadOut
from app.services import community_service as svc

router = APIRouter(tags=["community"])

_moderator = require_roles(Role.moderator, Role.instructor, Role.admin)


def _published_problem(db: Session, slug: str):
    problem = problems.get_published_by_slug(db, slug.strip().lower())
    if problem is None:
        raise AppError("PROBLEM_NOT_FOUND", "Problem not found.", 404)
    return problem


@router.get("/problems/{slug}/discussion", response_model=Envelope[list[ThreadOut]])
def list_discussion(
    slug: str,
    page: int = Query(1, ge=1, le=1000),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[list[ThreadOut]]:
    problem = _published_problem(db, slug)
    return Envelope(data=svc.list_threads(db, problem, user, page))


@router.post("/problems/{slug}/discussion", status_code=201, response_model=Envelope[PostOut])
def create_post(
    slug: str,
    payload: PostCreate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[PostOut]:
    # A few posts per minute stops floods without getting in the way of normal discussion.
    enforce_rate_limit(f"discuss:{user.id}", 6, 60)
    problem = _published_problem(db, slug)
    post = svc.create_post(
        db, user, problem, body=payload.body, parent_id=payload.parent_id, ip=client_ip(request)
    )
    return Envelope(data=svc._post_out(post, user.profile, user))


@router.delete("/discussion/{post_id}", response_model=Envelope[PostOut])
def delete_post(
    post_id: uuid.UUID,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[PostOut]:
    post = svc.get_post(db, post_id)
    post = svc.remove_post(db, user, post, ip=client_ip(request))
    profile = svc.author_profile(db, post)
    return Envelope(data=svc._post_out(post, profile, user))


@router.post("/discussion/{post_id}/report", status_code=201, response_model=Envelope[dict])
def report_post(
    post_id: uuid.UUID,
    payload: ReportCreate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[dict]:
    enforce_rate_limit(f"report:{user.id}", 10, 3600)
    post = svc.get_post(db, post_id)
    report = svc.report_post(db, user, post, payload.reason.strip(), ip=client_ip(request))
    return Envelope(data={"report_id": str(report.id), "status": report.status})


@router.get("/community/reports", response_model=Envelope[list[ReportOut]])
def list_reports(
    status: str = Query("open", pattern="^(open|dismissed|actioned)$"),
    _: User = Depends(_moderator),
    db: Session = Depends(get_db),
) -> Envelope[list[ReportOut]]:
    return Envelope(data=svc.list_reports(db, status))


@router.post("/community/reports/{report_id}/resolve", response_model=Envelope[dict])
def resolve_report(
    report_id: uuid.UUID,
    payload: ResolveIn,
    request: Request,
    user: User = Depends(_moderator),
    db: Session = Depends(get_db),
) -> Envelope[dict]:
    report = svc.get_report(db, report_id)
    report = svc.resolve_report(db, user, report, payload.action, ip=client_ip(request))
    return Envelope(data={"report_id": str(report.id), "status": report.status})
