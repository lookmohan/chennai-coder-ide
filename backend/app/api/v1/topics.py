from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import User
from app.schemas.common import Envelope
from app.services import topic_service as svc

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=Envelope[list[dict]])
def list_topics(_: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Envelope[list[dict]]:
    return Envelope(data=svc.summaries(db))


@router.get("/{slug}", response_model=Envelope[dict])
def topic_detail(slug: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Envelope[dict]:
    topic = svc.get_topic(slug.strip().lower())
    problems = svc.topic_problems(db, topic["slug"])
    # The same published counts as the list view, so both screens always agree.
    counts = {level: len(items) for level, items in problems.items()}
    return Envelope(data={**topic, "counts": counts, "problems": problems})
