from fastapi import FastAPI
from app.routes.routes import router as api_router
from app.config.db import Base, engine

app = FastAPI(
    title="Mini CRM API",
    description="""
    FastAPI + Celery + PostgreSQL tabanlı mini CRM backend.

    ### Özellikler
    - Kullanıcı kayıt & giriş (JWT Authentication)
    - Not oluşturma, listeleme, güncelleme, silme
    - Admin tüm notları görebilir
    - Kuyruk sistemi ile AI tabanlı özetleme
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
def startup():
    # Migration (alembic) kullanılmadığı durumda tabloyu otomatik yaratır.
    Base.metadata.create_all(bind=engine)
    print("✅ Veritabanına bağlandı.")


# tüm route'ları ekle
app.include_router(api_router)


@app.get("/", tags=["Health"])
def root():
    """API’nin canlı olduğunu test etmek için basit endpoint"""
    return {"message": "Mini CRM API çalışıyor 🚀"}








# Swagger UI:  http://127.0.0.1:8000/docs

# ReDoc:  http://127.0.0.1:8000/redoc