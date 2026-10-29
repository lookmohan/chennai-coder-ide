import uuid

from app.workers.celery_app import celery_app


@celery_app.task(name="judging.judge_submission")
def judge_submission_task(submission_id: str) -> None:
    from app.core.database import get_session_factory
    from app.services.judging import judge_submission

    db = get_session_factory()()
    try:
        judge_submission(db, uuid.UUID(submission_id))
    finally:
        db.close()
