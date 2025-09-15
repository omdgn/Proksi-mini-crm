# 🚀 Mini CRM with AI Summarization

A modern REST API backend built with FastAPI, featuring JWT authentication, role-based access control, and AI-powered note summarization using Hugging Face transformers.

## 🌐 Live Demo

**API Base URL:** https://proksi-mini-crm.onrender.com
**Interactive Docs:** https://proksi-mini-crm.onrender.com/docs

## ✨ Features

### 🔐 Authentication & Authorization
- **JWT-based authentication** with secure token generation
- **Role-based access control** (ADMIN/AGENT roles)
- **Password hashing** using bcrypt
- **Token expiration** management

### 📝 Note Management
- **CRUD operations** for notes with role-based filtering
- **AI-powered summarization** using Hugging Face BART model
- **Background processing** with Celery workers
- **Status tracking** (queued → processing → completed/failed)
- **Retry mechanism** with exponential backoff

### 🎁 Bonus Features
- **Bulk note creation** for batch operations
- **Advanced search** with keyword filtering
- **Statistics dashboard** with usage metrics
- **Pagination & filtering** for large datasets

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Message Queue:** Redis + Celery
- **AI Model:** Hugging Face Transformers (facebook/bart-large-cnn)
- **Containerization:** Docker + Docker Compose
- **Deployment:** Render (API) + Upstash (Redis)

### System Components
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │────│ PostgreSQL  │    │    Redis    │
│     API     │    │  Database   │    │   Message   │
│   Server    │    │             │    │   Queue     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                                      │
       │            ┌─────────────┐          │
       └────────────│   Celery    │──────────┘
                    │   Worker    │
                    │ (AI Tasks)  │
                    └─────────────┘
```

## 📡 API Endpoints

### Authentication
```http
POST /auth/register    # User registration
POST /auth/login       # User login
```

### Notes Management
```http
GET    /notes/         # List notes (role-filtered)
POST   /notes/         # Create note (triggers AI summarization)
GET    /notes/{id}     # Get specific note
PUT    /notes/{id}     # Update note
DELETE /notes/{id}     # Delete note
```

### Bonus Endpoints
```http
GET  /notes/stats      # Usage statistics
POST /notes/bulk       # Bulk note creation
GET  /notes/search     # Search notes by keyword
```

## 🚀 Quick Start

### 1. Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/omdgn/Proksi-mini-crm.git
cd Proksi-mini-crm

# Start all services
docker-compose up -d

# API will be available at http://localhost:8000
```

### 2. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload

# Start Celery worker (in another terminal)
celery -A celery_worker worker --loglevel=info
```

## 🧪 Testing the API

### 1. Register a User
```bash
curl -X POST "https://proksi-mini-crm.onrender.com/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

### 2. Login & Get Token
```bash
curl -X POST "https://proksi-mini-crm.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. Create Note (AI Summarization)
```bash
curl -X POST "https://proksi-mini-crm.onrender.com/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "This is a long text that will be automatically summarized by our AI system using advanced natural language processing techniques."
  }'
```

### 4. Check AI Summary Status
```bash
curl -X GET "https://proksi-mini-crm.onrender.com/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://host:port/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Services

- **API Server:** Port 8000
- **PostgreSQL:** Port 5433
- **Redis:** Port 6379
- **Celery Worker:** Background service

## 🤖 AI Summarization

The system uses **Hugging Face BART** model for intelligent text summarization:

- **Model:** `facebook/bart-large-cnn`
- **Processing:** Asynchronous via Celery
- **Fallback:** Rule-based summarization if AI fails
- **Retry Logic:** 3 attempts with exponential backoff

### Summarization Flow
1. User creates note → Status: `queued`
2. Celery picks up task → Status: `processing`
3. AI model generates summary → Status: `completed`
4. If error occurs → Status: `failed` (with retry)

## 📊 Database Schema

### Users Table
```sql
- id (UUID, Primary Key)
- email (VARCHAR, Unique)
- password (VARCHAR, Hashed)
- role (VARCHAR, ADMIN/AGENT)
- created_at (TIMESTAMP)
```

### Notes Table
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key)
- title (VARCHAR)
- content (TEXT)
- summary (TEXT, AI Generated)
- status (VARCHAR, queued/processing/completed/failed)
- error (VARCHAR, Error message if failed)
- created_at (TIMESTAMP)
```

## 🛡️ Security Features

- **Password hashing** with bcrypt
- **JWT token authentication**
- **Role-based authorization**
- **Environment-based secrets**
- **SQL injection protection** (SQLAlchemy ORM)
- **CORS configuration**

## 🚀 Deployment

### Production Stack
- **API:** Render Web Service
- **Database:** Render PostgreSQL
- **Cache/Queue:** Upstash Redis
- **Worker:** Render Background Worker

### CI/CD Ready
- **Docker containers** for consistent deployments
- **Environment-based configuration**
- **Health checks** and monitoring
- **Auto-scaling** support

## 📈 Performance & Scalability

- **Async processing** for AI tasks
- **Connection pooling** for database
- **Redis caching** for sessions
- **Horizontal scaling** with multiple workers
- **Resource optimization** with Docker

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent async web framework
- **Hugging Face** for providing state-of-the-art AI models
- **Render** for reliable cloud hosting
- **SQLAlchemy** for robust ORM functionality

---

**Built with ❤️ for modern CRM solutions**