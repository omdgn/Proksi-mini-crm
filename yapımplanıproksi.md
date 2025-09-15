# ✅ Mini-CRM Backend Yol Haritası (FastAPI + Celery + PostgreSQL + Redis)

---

## 📦 1. Proje İskeleti & Ortam Kurulumu

- [x] Python, pip, git, docker kontrolü
- [x] Proje klasörü oluştur: `proksi-test-case/mini-crm`
- [x] VS Code ile aç
- [x] `.venv` oluştur ve aktive et
- [x] `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `psycopg2-binary` vs. kur
- [x] `requirements.txt` oluştur

---

## 🏗️ 2. Klasör Yapısı

- [x] `app/` ana klasörü oluştur
- [x] Alt klasörler:
  - [x] `controllers/`
  - [x] `routes/`
  - [x] `models/`
  - [x] `schemas/`
  - [x] `services/`
  - [x] `config/`
  - [x] Ana dosyalar:
  - [x] `main.py`
  - [x] `dependencies.py`

---

## ⚙️ 3. Yapılandırma Katmanı

- [x] `settings.py` (.env yükleyici)
- [x] `db.py` (SQLAlchemy bağlantı)
- [x] `celery_config.py` (Redis için Celery ayarları)

---

## 🧩 4. Modeller & Şemalar

- [x] `user.model.py` → `id`, `email`, `password`, `role`, `created_at`
- [x] `note.model.py` → `id`, `user_id`, `title`, `content`, `summary`, `status`, `error`
- [x] `auth.schema.py` → `SignupRequest`, `LoginRequest`, `TokenResponse`
- [x] `note.schema.py` → `NoteCreate`, `NoteResponse`, `NoteUpdate` *(bonus)*
- [x] `NoteBulkCreate`, `NoteBulkResponse`, `NoteStats` *(bonus schemas)*

---

## 🔐 5. Kimlik Doğrulama & Yetkilendirme

- [x] `token.service.py` → JWT oluştur/çöz
- [x] `dependencies.py` → `get_current_user`, `require_admin`

---

## 🧠 6. Controller'lar

- [x] `auth.controller.py` → `signup()`, `login()`
- [x] `note.controller.py` →
  - `create_note()`
  - `get_notes()` → **role bazlı filtreleme**
  - `get_note_by_id()`
  - `update_note()` *(bonus)*
  - `delete_note()` *(bonus)*
  - `get_note_stats()` *(bonus)*
  - `create_bulk_notes()` *(bonus)*
  - `search_notes()` *(bonus)*

---

## 🌐 7. Routes

- [x] `auth.route.py` → `/auth/signup`, `/auth/login`
- [x] `note.route.py` → `/notes`, `/notes/{id}`, `/notes/{id}/delete`
- [x] `routes.py` → route'ları birleştir
- [x] `main.py` → FastAPI app tanımı + route'lar + middleware

---

## 🤖 8. Özetleme & Kuyruk Sistemi (AI)

- [ ] `summarize.service.py` → Huggingface LLM kullanımı
- [ ] `tasks.py` → `summarize_note_task(note_id)`
- [ ] `celery_worker.py` → Celery worker giriş dosyası
- [ ] **Retry & idempotency mekanizması ekle** ✅

---

## 📥 9. Migration

- [x] `alembic init`
- [x] `env.py` içindeki `target_metadata` ayarı
- [x] `alembic revision --autogenerate`
- [x] `alembic upgrade head`

---

## 🐳 10. Docker & Compose

- [ ] `Dockerfile` (API)
- [ ] `Dockerfile.worker` (Celery Worker)
- [ ] `docker-compose.yml` → API + PostgreSQL + Redis + Worker
- [ ] `.env` → tüm servis ayarları

---

## 🧪 11. Test & Dokümantasyon

- [ ] `/docs` (Swagger) temiz açıklamalar + response_model'ler
- [ ] `tests/` klasörü oluştur
- [ ] `pytest` ile temel testler (auth, note, task)

---

## 🚀 12. Deployment & CI/CD

- [ ] Koyeb veya Railway deploy
- [ ] GitHub Actions: push sonrası otomatik build + deploy

---

## 🎥 13. Loom Videosu

- [ ] Tüm endpoint’lerin canlı testi
- [ ] Kod yapısının anlatımı
- [ ] Docker + worker çalışma mantığı
- [ ] `.env` ve yapılandırma anlatımı

---

## 🎁 Bonus Özellikler (Yaparsan ekstra puan)

- [x] `PUT /notes/{id}` → Not güncelleme
- [x] `DELETE /notes/{id}` → Not silme (soft/hard)
- [x] `/notes?status=completed&limit=10` → Pagination + filtreleme
- [x] `GET /notes/stats` → Kullanıcı not istatistikleri *(yeni bonus)*
- [x] `POST /notes/bulk` → Toplu not ekleme *(yeni bonus)*
- [x] `GET /notes/search?q=keyword` → Not arama *(yeni bonus)*
- [ ] Role-based UI planı (geliştirme yok, sadece açıklama)
- [ ] Swagger açıklamaları ve örnek yanıtlar
- [ ] `POST /notes` işlemi idempotent hale getirme (`hash` + Redis?)

