from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import User
from app.schemas.common import Envelope
from app.schemas.community import PostOut
from app.services.community_feed import latest_threads

router = APIRouter(prefix="/community", tags=["community"])


class LatestThreadOut(BaseModel):
    post: PostOut
    problem_slug: str
    problem_title: str
    reply_count: int


@router.get("/latest", response_model=Envelope[list[LatestThreadOut]])
def latest(
    page: int = Query(1, ge=1, le=1000),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Envelope[list[LatestThreadOut]]:
    return Envelope(data=[LatestThreadOut(**row) for row in latest_threads(db, user, page)])
