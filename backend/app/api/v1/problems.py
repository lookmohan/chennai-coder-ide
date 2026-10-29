from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.errors import AppError
from app.models import User
from app.repositories import problem_repository as problems
from app.schemas.common import Envelope, PageMeta
from app.schemas.problem import ProblemDetail, ProblemListItem
from app.services import problem_service
from app.services.judge0_client import get_judge_client

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=Envelope[list[ProblemListItem]])
def list_problems(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    q: str | None = Query(None, max_length=100),
    difficulty: str | None = Query(None, pattern="^(Easy|Medium|Hard)$"),
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[list[ProblemListItem]]:
    rows, total = problems.list_published(db, page=page, page_size=page_size, q=q, difficulty=difficulty)
    return Envelope(
        data=[problem_service.to_list_item(p) for p in rows],
        meta=PageMeta(page=page, page_size=page_size, total=total).model_dump(),
    )


@router.get("/{slug}", response_model=Envelope[ProblemDetail])
def get_problem(
    slug: str,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[ProblemDetail]:
    problem = problems.get_published_by_slug(db, slug.strip().lower())
    if problem is None:
        raise AppError("PROBLEM_NOT_FOUND", "Problem not found.", 404)
    return Envelope(
        data=problem_service.to_detail(problem, execution_available=get_judge_client().configured)
    )
