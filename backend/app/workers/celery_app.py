from celery import Celery

from app.core.config import get_settings

_settings = get_settings()

celery_app = Celery(
    "chennai_coder",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=["app.workers.judging_tasks"],
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=120,
    timezone="UTC",
)


@celery_app.task(name="system.ping")
def ping() -> str:
    return "pong"
