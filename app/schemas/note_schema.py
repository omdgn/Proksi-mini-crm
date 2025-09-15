from pydantic import BaseModel, constr
from typing import Optional, List
from uuid import UUID

class NoteCreate(BaseModel):
    title: constr(min_length=3)  # type: ignore
    content: constr(min_length=10)  # type: ignore

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Toplantı Notları",
                "content": "Bugün müşteri ile ürün lansman planını konuştuk."
            }
        }


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Güncellenmiş Başlık",
                "content": "Notun içeriğini değiştirdim."
            }
        }


class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: str
    summary: Optional[str] = None
    status: str
    error: Optional[str] = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Toplantı Notları",
                "content": "Bugün müşteri ile ürün lansman planını konuştuk.",
                "summary": "Ürün lansmanı planlandı.",
                "status": "completed",
                "error": None
            }
        }


class NoteBulkCreate(BaseModel):
    notes: List[NoteCreate]

    class Config:
        json_schema_extra = {
            "example": {
                "notes": [
                    {
                        "title": "İlk Not",
                        "content": "Bu ilk notun içeriği"
                    },
                    {
                        "title": "İkinci Not",
                        "content": "Bu ikinci notun içeriği"
                    }
                ]
            }
        }


class NoteBulkResponse(BaseModel):
    created_count: int
    notes: List[NoteResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "created_count": 2,
                "notes": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "İlk Not",
                        "content": "Bu ilk notun içeriği",
                        "status": "pending"
                    }
                ]
            }
        }


class NoteStats(BaseModel):
    total_notes: int
    pending_notes: int
    processing_notes: int
    completed_notes: int
    failed_notes: int

    class Config:
        json_schema_extra = {
            "example": {
                "total_notes": 25,
                "pending_notes": 3,
                "processing_notes": 1,
                "completed_notes": 20,
                "failed_notes": 1
            }
        }
