from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.schemas.common import Envelope

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=Envelope[dict])
def liveness() -> Envelope[dict]:
    return Envelope(data={"status": "ok"})


@router.get("/ready", response_model=Envelope[dict])
def readiness(db: Session = Depends(get_db)) -> Envelope[dict]:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise AppError("DATABASE_UNAVAILABLE", "Database is unavailable.", 503)
    return Envelope(data={"status": "ready"})
