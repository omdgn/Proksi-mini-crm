from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.config.db import Base

class Note(Base):
    """
    Not tablosu.
    - Kullanıcıların oluşturduğu notları saklar.
    - 'summary' alanı Celery worker tarafından doldurulur.
    - 'status' alanı: pending | processing | completed | failed
    """
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
