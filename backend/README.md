# Student360 FastAPI Backend

Centralized Student Intelligence & Portfolio Platform Backend built using FastAPI, SQLAlchemy, and Supabase.

---

## Backend Stack
- **Framework**: FastAPI (Asynchronous Python Web framework)
- **Database ORM**: SQLAlchemy
- **Database Hosted Provider**: Supabase (PostgreSQL)
- **Database Migrations**: Alembic
- **Storage Handler**: Supabase Storage Buckets (Local uploads directory fallback)
- **Authentication**: JWT tokens (JSON Web Tokens) with jose & passlib
- **Excel Parser**: openpyxl / pandas

---

## Folder Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── score.py
│   │   ├── submission.py
│   │   ├── resume.py
│   │   ├── profile.py
│   │   ├── portfolio.py
│   │   └── ai_summary.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── student.py
│   │   ├── score.py
│   │   ├── submission.py
│   │   ├── resume.py
│   │   ├── profile.py
│   │   ├── portfolio.py
│   │   └── ai.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── students.py
│   │   ├── scores.py
│   │   ├── leaderboard.py
│   │   ├── recommendations.py
│   │   ├── mentor.py
│   │   ├── submissions.py
│   │   ├── resume.py
│   │   ├── profile.py
│   │   ├── portfolio.py
│   │   ├── ai.py
│   │   └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── analytics_service.py
│   │   ├── leaderboard_service.py
│   │   ├── upload_service.py
│   │   ├── portfolio_service.py
│   │   ├── recommendation_service.py
│   │   └── ai_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── file_utils.py
│   │   ├── response_utils.py
│   │   └── domain_utils.py
│   └── seed.py
├── alembic/
├── uploads/
│   ├── profile/
│   ├── resumes/
│   ├── projects/
│   ├── certificates/
│   └── achievements/
├── requirements.txt
├── .env.example
├── alembic.ini
└── README.md
```

---

## Supabase Setup

1. **Create Supabase Project**:
   - Go to [Supabase Console](https://supabase.com/) and create a new project.
2. **Retrieve Connection URI**:
   - Go to **Project Settings** -> **Database** -> **Connection Strings**.
   - Copy the Transaction Pooler or Direct connection URI.
3. **Configure Environment File**:
   - Create `.env` inside `backend/` copied from `.env.example`.
   - Update `DATABASE_URL` with your Supabase connection string:
     `DATABASE_URL=postgresql://postgres:<PASSWORD>@db.<REF>.supabase.co:5432/postgres`
4. **Create Supabase Storage Bucket**:
   - Open the **Storage** section in your Supabase console dashboard.
   - Create a new public bucket named `student360-uploads`.
   - Populate `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, and `SUPABASE_STORAGE_BUCKET` in your `.env`.

---

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
Run Alembic commands from the `backend/` folder to setup the schemas inside Supabase Hosted PostgreSQL:
```bash
alembic revision --autogenerate -m "initial student360 schema"
alembic upgrade head
```

### 3. Seed Database Data
Populate standard roles and 10 default students inside the database:
```bash
python -m app.seed
```

### 4. Run the Backend Server
Start the Uvicorn web server:
```bash
uvicorn app.main:app --reload
```

---

## API List

- **Health Checks**: `GET /health`
- **Auth**:
  - `POST /auth/login`
  - `GET /auth/me`
  - `POST /auth/refresh`
  - `POST /auth/logout`
- **Students**:
  - `GET /students`
  - `GET /students/{id_or_register_no}`
  - `GET /students/{id_or_register_no}/performance`
  - `GET /students/recommend`
  - `GET /students/{register_no}/about`
  - `PUT /students/{register_no}/about`
- **Excel Upload**: `POST /scores/upload`
- **Leaderboard**:
  - `GET /leaderboard/overall`
  - `GET /leaderboard/domain/{domain}`
- **Submissions**:
  - `POST/GET /student/projects`
  - `POST/GET /student/certifications`
  - `POST/GET /student/achievements`
- **Resumes**:
  - `GET/POST/PUT /students/{register_no}/resume`
- **Mentor Workflow**:
  - `GET /mentor/pending`
  - `GET /mentor/approvals`
  - `PUT /mentor/review`
- **Profiles**:
  - `GET /users/me/profile`
  - `PUT /users/me/profile`
  - `POST /users/me/profile-image`
- **Public Portfolios**:
  - `GET /portfolio/{register_no}`
  - `GET/PUT /portfolio/customization/{register_no}`
- **AI Intelligence**:
  - `POST /ai/generate-summary`
  - `POST /ai/faculty-query`
- **Admin Panel**:
  - `GET /admin/overview`
  - Full CRUD operations for Users, Students, Faculty, Mentors, and Mentor Assignments under `/admin`.

---

## Demo Login Credentials
All seed users share the same default password: **`Password123!`**

- **Student**: `student@example.com` or `22AD001` (Shahul)
- **Faculty**: `faculty@example.com` (Dr. Ramanujam)
- **Mentor**: `mentor@example.com` (Prof. Priya)
- **Placement Mentor**: `placement@example.com` (Lead Training Officer)
- **Admin**: `admin@example.com` (Admin Officer)

---

## Frontend Connection Guide
The backend runs at `http://localhost:8000`. Set the baseURL in your frontend `src/services/api.js` to match the backend URL.
No frontend code needs modifications to support the backend routing layers.

---

## AI Fallback & Ollama Integration

The AI features (Student performance summaries and Faculty query intents) use a layered execution approach:
1. **Rule-Based Fallback (Default)**: Automatically computes strengths, weaknesses, and placement recommendations using deterministic database thresholds. No API keys, Internet connection, or active Ollama instances are required.
2. **Ollama Integration (Optional)**: If `LLM_PROVIDER=ollama` is configured and an Ollama instance is active at `OLLAMA_BASE_URL` with `OLLAMA_MODEL`, the backend will leverage the local LLM to format and rephrase the rule-based metrics into conversational summaries. If the instance is unreachable, it silently falls back to the deterministic generation.

---

## Final Manual Testing Guide

Verify your deployed API server using these endpoints:

### 1. System Health Check
```bash
curl -X GET http://localhost:8000/health
```

### 2. Login & Token Retrieval
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "22AD001", "password": "Password123!"}'
```

### 3. Check Logged-in User
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 4. Fetch Students List
```bash
curl -X GET http://localhost:8000/students
```

### 5. Fetch Specific Student Profile
```bash
curl -X GET http://localhost:8000/students/22AD001
```

### 6. Fetch Student Test History
```bash
curl -X GET http://localhost:8000/students/22AD001/performance
```

### 7. Fetch Overall Leaderboard
```bash
curl -X GET http://localhost:8000/leaderboard/overall
```

### 8. Fetch DBMS Leaderboard
```bash
curl -X GET http://localhost:8000/leaderboard/domain/DBMS
```

### 9. Fetch Domain Recommendations
```bash
curl -X GET "http://localhost:8000/students/recommend?domain=DSA&limit=10"
```

### 10. Fetch Pending Submissions
```bash
curl -X GET http://localhost:8000/mentor/pending \
  -H "Authorization: Bearer <MENTOR_ACCESS_TOKEN>"
```

### 11. Fetch Public Portfolio
```bash
curl -X GET http://localhost:8000/portfolio/22AD001
```

### 12. Generate Student Performance Summary
```bash
curl -X POST http://localhost:8000/ai/generate-summary \
  -H "Content-Type: application/json" \
  -d '{"register_no": "22AD001"}'
```

### 13. Query Faculty AI Assistant
```bash
curl -X POST http://localhost:8000/ai/faculty-query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <FACULTY_ACCESS_TOKEN>" \
  -d '{"query": "Top 10 DSA students"}'
```

