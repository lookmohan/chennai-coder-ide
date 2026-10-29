import uuid

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.core.rate_limit import client_ip
from app.models import Role, User
from app.repositories import user_repository as users
from app.schemas.admin import AuditOut, OverviewOut, ProblemAdminOut, ProblemIn, ProblemRowOut, StatusIn
from app.schemas.common import Envelope, PageMeta
from app.schemas.user import StudentRow
from app.services import admin_problem_service as svc

router = APIRouter(prefix="/admin", tags=["admin"])

# Instructors and admins can view. Only admins can change anything.
_staff = require_roles(Role.instructor, Role.admin)
_admin = require_roles(Role.admin)


@router.get("/overview", response_model=Envelope[OverviewOut])
def overview(_: User = Depends(_staff), db: Session = Depends(get_db)) -> Envelope[OverviewOut]:
    return Envelope(data=OverviewOut(**svc.overview(db)))


@router.get("/students", response_model=Envelope[list[StudentRow]])
def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    q: str | None = Query(None, max_length=100),
    _: User = Depends(_staff),
    db: Session = Depends(get_db),
) -> Envelope[list[StudentRow]]:
    rows, total = users.list_students(db, page=page, page_size=page_size, query=q)
    data = [
        StudentRow(
            id=u.id,
            email=u.email,
            username=p.username,
            display_name=p.display_name,
            status=u.status,
            created_at=u.created_at,
            last_login_at=u.last_login_at,
        )
        for u, p in rows
    ]
    return Envelope(data=data, meta=PageMeta(page=page, page_size=page_size, total=total).model_dump())


@router.get("/problems", response_model=Envelope[list[ProblemRowOut]])
def list_problems(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    q: str | None = Query(None, max_length=100),
    status: str | None = Query(None, pattern="^(draft|published|archived)$"),
    _: User = Depends(_staff),
    db: Session = Depends(get_db),
) -> Envelope[list[ProblemRowOut]]:
    rows, total = svc.list_problems(db, page=page, page_size=page_size, q=q, status=status)
    return Envelope(
        data=[svc.to_row_out(p) for p in rows],
        meta=PageMeta(page=page, page_size=page_size, total=total).model_dump(),
    )


@router.get("/problems/{problem_id}", response_model=Envelope[ProblemAdminOut])
def get_problem(problem_id: uuid.UUID, _: User = Depends(_staff), db: Session = Depends(get_db)) -> Envelope[ProblemAdminOut]:
    # Staff can see hidden tests here, because this page is for editing. Students never reach it.
    return Envelope(data=svc.to_admin_out(svc.get_problem(db, problem_id)))


@router.post("/problems", status_code=201, response_model=Envelope[ProblemAdminOut])
def create_problem(
    payload: ProblemIn,
    request: Request,
    user: User = Depends(_admin),
    db: Session = Depends(get_db),
) -> Envelope[ProblemAdminOut]:
    problem = svc.create_problem(db, user, payload, ip=client_ip(request))
    return Envelope(data=svc.to_admin_out(problem))


@router.put("/problems/{problem_id}", response_model=Envelope[ProblemAdminOut])
def update_problem(
    problem_id: uuid.UUID,
    payload: ProblemIn,
    request: Request,
    user: User = Depends(_admin),
    db: Session = Depends(get_db),
) -> Envelope[ProblemAdminOut]:
    problem = svc.get_problem(db, problem_id)
    problem = svc.update_problem(db, user, problem, payload, ip=client_ip(request))
    return Envelope(data=svc.to_admin_out(problem))


@router.post("/problems/{problem_id}/status", response_model=Envelope[ProblemAdminOut])
def set_problem_status(
    problem_id: uuid.UUID,
    payload: StatusIn,
    request: Request,
    user: User = Depends(_admin),
    db: Session = Depends(get_db),
) -> Envelope[ProblemAdminOut]:
    problem = svc.get_problem(db, problem_id)
    problem = svc.set_status(db, user, problem, payload.status, ip=client_ip(request))
    return Envelope(data=svc.to_admin_out(problem))


@router.get("/audit", response_model=Envelope[list[AuditOut]])
def audit(
    limit: int = Query(50, ge=1, le=200),
    _: User = Depends(_admin),
    db: Session = Depends(get_db),
) -> Envelope[list[AuditOut]]:
    rows = svc.recent_audit(db, limit)
    return Envelope(
        data=[
            AuditOut(
                id=r.id,
                action=r.action,
                entity_type=r.entity_type,
                entity_id=r.entity_id,
                actor_id=r.actor_id,
                metadata=r.metadata_,
                ip=r.ip,
                created_at=r.created_at,
            )
            for r in rows
        ]
    )
