from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.core.errors import AppError
from app.core.rate_limit import client_ip, enforce_rate_limit
from app.models import User
from app.repositories import submission_repository as submissions
from app.schemas.common import Envelope
from app.schemas.submission import SubmissionCreate, SubmissionOut
from app.services import submission_service
import uuid


def _require_submissions_enabled() -> None:
    """Server-side submissions are off by default. Practice runs in the browser instead."""
    if not get_settings().submissions_enabled:
        raise AppError(
            "SUBMISSIONS_DISABLED",
            "Server-side submissions are turned off. Practice runs in your browser.",
            404,
        )


# Router-level dependency: runs before anything else, so the endpoints look absent when disabled.
router = APIRouter(prefix="/submissions", tags=["submissions"], dependencies=[Depends(_require_submissions_enabled)])


@router.post("", status_code=202, response_model=Envelope[SubmissionOut])
def create_submission(
    payload: SubmissionCreate,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[SubmissionOut]:
    enforce_rate_limit(f"submit:{user.id}", get_settings().submission_rate_per_minute, 60)
    sub = submission_service.create_submission(
        db,
        user,
        problem_slug=payload.problem_slug.strip().lower(),
        language=payload.language.strip().lower(),
        source_code=payload.source_code,
        ip=client_ip(request),
    )
    return Envelope(data=submission_service.to_output(db, sub))


@router.get("/{submission_id}", response_model=Envelope[SubmissionOut])
def get_submission(
    submission_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[SubmissionOut]:
    sub = submissions.get_for_user(db, submission_id, user.id)
    if sub is None:
        raise AppError("SUBMISSION_NOT_FOUND", "Submission not found.", 404)
    return Envelope(data=submission_service.to_output(db, sub))
