import logging
import threading
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_session_factory
from app.core.errors import AppError
from app.models import Problem, Submission, SubmissionStatus as S, User
from app.repositories import problem_repository as problems
from app.schemas.submission import SubmissionOut
from app.services import audit_service
from app.services.judge0_client import SUPPORTED_LANGUAGES, get_judge_client
from app.services.judging import judge_submission

logger = logging.getLogger("app.submissions")


def enqueue_judging(submission_id: uuid.UUID) -> None:
    if get_settings().queue_mode == "celery":
        from app.workers.judging_tasks import judge_submission_task

        judge_submission_task.delay(str(submission_id))
        return

    threading.Thread(
        target=_judge_in_background,
        args=(submission_id,),
        daemon=True,
        name=f"judge-{submission_id}",
    ).start()


def _judge_in_background(submission_id: uuid.UUID) -> None:
    db = get_session_factory()()
    try:
        judge_submission(db, submission_id)
    except Exception:
        logger.exception("background_judging_failed", extra={"submission_id": str(submission_id)})
    finally:
        db.close()


def create_submission(
    db: Session,
    user: User,
    *,
    problem_slug: str,
    language: str,
    source_code: str,
    ip: str | None,
) -> Submission:
    if not get_judge_client().configured:
        raise AppError(
            "EXECUTION_NOT_CONFIGURED",
            "Code execution isn't set up on this server yet, so submissions are paused.",
            503,
        )

    problem = problems.get_published_by_slug(db, problem_slug)
    if problem is None:
        raise AppError("PROBLEM_NOT_FOUND", "Problem not found.", 404)
    if language not in SUPPORTED_LANGUAGES or language not in (problem.starter_code or {}):
        raise AppError("LANGUAGE_NOT_SUPPORTED", "This problem doesn't support that language.", 422)
    if not problem.test_cases:
        raise AppError("PROBLEM_NOT_READY", "This problem doesn't have test cases yet.", 409)

    sub = Submission(
        user_id=user.id,
        problem_id=problem.id,
        language=language,
        source_code=source_code,
        status=S.queued.value,
        total_count=len(problem.test_cases),
    )
    db.add(sub)
    db.flush()
    # Metadata deliberately excludes the source code.
    audit_service.record(
        db,
        "submission.create",
        actor_id=user.id,
        entity_type="submission",
        entity_id=str(sub.id),
        metadata={"problem_slug": problem.slug, "language": language},
        ip=ip,
    )
    db.commit()
    db.refresh(sub)

    try:
        enqueue_judging(sub.id)
    except Exception:
        logger.exception("enqueue_failed", extra={"submission_id": str(sub.id)})
        sub.status = S.system_error.value
        sub.message = "Could not queue your submission. Please try again."
        sub.judged_at = datetime.now(timezone.utc)
        db.commit()
        raise AppError("QUEUE_UNAVAILABLE", "Couldn't queue your submission. Please try again.", 503)

    return sub


def to_output(db: Session, sub: Submission) -> SubmissionOut:
    problem = db.get(Problem, sub.problem_id)
    return SubmissionOut(
        id=sub.id,
        problem_slug=problem.slug,
        language=sub.language,
        source_code=sub.source_code,
        status=sub.status,
        passed_count=sub.passed_count,
        total_count=sub.total_count,
        failed_test_position=sub.failed_test_position,
        runtime_ms=sub.runtime_ms,
        memory_kb=sub.memory_kb,
        message=sub.message,
        created_at=sub.created_at,
        judged_at=sub.judged_at,
    )
