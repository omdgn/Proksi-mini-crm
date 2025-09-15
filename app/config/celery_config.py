from celery import Celery
from app.config.settings import settings

celery_app = Celery(
    "mini_crm",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Istanbul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # maksimum 5 dakika çalışabilir
)
