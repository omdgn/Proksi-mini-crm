from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from app.schemas.note_schema import NoteCreate, NoteResponse, NoteUpdate, NoteBulkCreate, NoteBulkResponse, NoteStats
from app.models.note_model import Note
from app.dependencies import get_db, get_current_user
from app.models.user_model import User
from app.tasks import summarize_note_task

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni not oluştur",
    description="Kullanıcı yeni bir not oluşturur. Not başlangıçta `queued` durumunda olur ve özetleme kuyruğa alınır."
)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = Note(
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
        status="queued"
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    # Queue the summarization task
    print(f"🔍 DEBUG: Attempting to queue task for note {note.id}")
    try:
        task_result = summarize_note_task.delay(note.id)
        print(f"✅ DEBUG: Task queued successfully for note {note.id}: {task_result.id}")
    except Exception as e:
        # If queuing fails, update note status to failed
        print(f"❌ DEBUG: Exception occurred: {e}")
        note.status = "failed"
        note.error_message = f"Failed to queue task: {str(e)}"
        db.commit()
        raise  # Re-raise to see the error

    return note


@router.get(
    "/",
    response_model=list[NoteResponse],
    summary="Notları listele (pagination + filtreleme destekli)",
    description="""
    - Admin tüm notları görebilir.
    - Normal kullanıcı sadece kendi notlarını görebilir.
    - Opsiyonel `status` parametresi ile filtreleme yapılabilir.
    - Opsiyonel `limit` parametresi ile sonuç sayısı sınırlandırılabilir.
    """
)
def get_notes(
    status: str | None = Query(default=None, description="Filtrelemek için not durumu (pending, completed, failed)"),
    limit: int = Query(default=10, ge=1, le=100, description="Döndürülecek maksimum sonuç sayısı"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Note)

    # rol bazlı filtre
    if current_user.role != "admin":
        query = query.filter(Note.user_id == current_user.id)

    # status filtresi
    if status:
        query = query.filter(Note.status == status)

    notes = query.limit(limit).all()
    return notes


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Tek not getir",
    description="ID'si verilen notu döner. Normal kullanıcı sadece kendi notunu görebilir."
)
def get_note_by_id(note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user.role != "admin" and note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return note


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Not güncelle",
    description="Kullanıcı kendi notunu güncelleyebilir. Admin tüm notları güncelleyebilir."
)
def update_note(note_id: UUID, payload: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user.role != "admin" and note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    note.title = payload.title or note.title
    note.content = payload.content or note.content
    db.commit()
    db.refresh(note)
    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Not sil",
    description="Kullanıcı kendi notunu silebilir. Admin tüm notları silebilir."
)
def delete_note(note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user.role != "admin" and note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(note)
    db.commit()
    return None


@router.get(
    "/stats",
    response_model=NoteStats,
    summary="Not istatistiklerini getir",
    description="Kullanıcının not istatistiklerini döner. Admin tüm notların istatistiklerini görebilir."
)
def get_note_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Note)

    # Role-based filtering
    if current_user.role != "admin":
        query = query.filter(Note.user_id == current_user.id)

    # Get total count
    total_notes = query.count()

    # Get counts by status
    pending_notes = query.filter(Note.status == "pending").count()
    processing_notes = query.filter(Note.status == "processing").count()
    completed_notes = query.filter(Note.status == "completed").count()
    failed_notes = query.filter(Note.status == "failed").count()

    return NoteStats(
        total_notes=total_notes,
        pending_notes=pending_notes,
        processing_notes=processing_notes,
        completed_notes=completed_notes,
        failed_notes=failed_notes
    )


@router.post(
    "/bulk",
    response_model=NoteBulkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Toplu not oluştur",
    description="Birden fazla notu aynı anda oluşturur. Tüm notlar başlangıçta 'pending' durumunda olur."
)
def create_bulk_notes(payload: NoteBulkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    created_notes = []

    for note_data in payload.notes:
        note = Note(
            user_id=current_user.id,
            title=note_data.title,
            content=note_data.content,
            status="pending"
        )
        db.add(note)
        created_notes.append(note)

    db.commit()

    # Refresh all notes to get their IDs
    for note in created_notes:
        db.refresh(note)

    return NoteBulkResponse(
        created_count=len(created_notes),
        notes=created_notes
    )


@router.get(
    "/search",
    response_model=list[NoteResponse],
    summary="Notları ara",
    description="Başlık ve içerikte anahtar kelime arar. Admin tüm notlarda arayabilir."
)
def search_notes(
    q: str = Query(..., min_length=1, description="Aranacak anahtar kelime"),
    limit: int = Query(default=10, ge=1, le=100, description="Döndürülecek maksimum sonuç sayısı"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Note)

    # Role-based filtering
    if current_user.role != "admin":
        query = query.filter(Note.user_id == current_user.id)

    # Search in title and content (case insensitive)
    search_filter = (
        Note.title.ilike(f"%{q}%") |
        Note.content.ilike(f"%{q}%")
    )

    notes = query.filter(search_filter).limit(limit).all()
    return notes


