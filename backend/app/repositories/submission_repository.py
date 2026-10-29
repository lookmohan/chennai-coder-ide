import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Submission


def get_for_user(db: Session, submission_id: uuid.UUID, user_id: uuid.UUID) -> Submission | None:
    """Scoped by owner: another student's submission looks exactly like a missing one."""
    return db.scalar(select(Submission).where(Submission.id == submission_id, Submission.user_id == user_id))
