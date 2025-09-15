from celery import Celery
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.config.settings import settings
from app.models.note_model import Note
from app.services.summarize_service import SummarizeService
import logging
import time

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'mini-crm',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_default_retry_delay=60,  # 1 minute
    task_max_retries=3,
    # Prevent duplicate task execution
    task_reject_on_worker_lost=True,
    task_acks_late=True,
)

@celery_app.task(bind=True)
def summarize_note_task(self, note_id: int):
    """
    Background task to summarize a note
    Includes retry mechanism and idempotency
    """
    db: Session = next(get_db())

    try:
        # Get note from database
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            logger.error(f"Note with id {note_id} not found")
            return {"error": "Note not found", "note_id": note_id}

        # Check if already completed (idempotency)
        if note.status == "completed":
            logger.info(f"Note {note_id} already completed, skipping")
            return {
                "note_id": note_id,
                "status": "completed",
                "summary": note.summary,
                "message": "Already completed"
            }

        # Update status to processing
        note.status = "processing"
        note.error_message = None
        db.commit()

        logger.info(f"Starting summarization for note {note_id}")

        # Initialize summarization service
        summarize_service = SummarizeService()

        # Simulate some processing time (optional)
        time.sleep(2)

        # Generate summary
        summary = summarize_service.summarize_text(note.content)

        if summary:
            # Update note with summary and mark as completed
            note.summary = summary
            note.status = "completed"
            note.error_message = None

            db.commit()
            logger.info(f"Successfully summarized note {note_id}")

            return {
                "note_id": note_id,
                "status": "completed",
                "summary": summary
            }
        else:
            raise Exception("Failed to generate summary")

    except Exception as exc:
        logger.error(f"Summarization failed for note {note_id}: {exc}")

        # Update note status to failed
        try:
            note = db.query(Note).filter(Note.id == note_id).first()
            if note:
                note.status = "failed"
                note.error_message = str(exc)
                db.commit()
        except Exception as db_exc:
            logger.error(f"Failed to update note status: {db_exc}")

        # Retry task with exponential backoff
        if self.request.retries < self.max_retries:
            retry_countdown = 60 * (2 ** self.request.retries)
            logger.info(f"Retrying summarization for note {note_id} in {retry_countdown}s (attempt {self.request.retries + 1})")
            raise self.retry(exc=exc, countdown=retry_countdown)

        return {
            "error": f"Max retries exceeded: {exc}",
            "note_id": note_id,
            "retries": self.request.retries
        }

    finally:
        db.close()