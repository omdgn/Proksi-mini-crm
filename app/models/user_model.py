from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.config.db import Base

class User(Base):
    """
    Kullanıcı tablosu.
    - Sisteme kayıtlı kullanıcıların email, şifre ve rol bilgilerini tutar.
    - Roller: 'user' ve 'admin'.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
