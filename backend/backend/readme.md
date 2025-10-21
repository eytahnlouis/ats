# 🧠 ATS Project — Backend (Django REST API)

> A modern Applicant Tracking System (ATS) built with **Django REST Framework**.\
> This backend powers the job posting, resume upload, and candidate scoring logic for the full-stack app.

---

## ⚙️ Tech Stack

- **Python 3.12**
- **Django 5+**
- **Django REST Framework (DRF)**
- **SimpleJWT** (for authentication)
- **django-cors-headers**
- **SQLite3** (dev) / PostgreSQL (prod ready)
- **uuid** for unique object IDs

---

## 🧬 Project Structure

```
backend/
│
├── backend/
│   ├── settings.py         ← global settings & CORS config
│   ├── urls.py             ← root routing
│   └── wsgi.py
│
├── cvs/
│   ├── models.py           ← Job, Candidate, Resume, Keyword
│   ├── views.py            ← API endpoints
│   ├── serializers.py      ← data transformation
│   ├── urls.py             ← /api/cvs/ routes
│   └── services/
│       └── parsing.py      ← text extraction from resumes
|       └── scoring.py      ← scoring algorithm
│
└── manage.py
│
└── db.sqlite3              ← database storing all infos

```

---

## 📚 Models Overview

### 🏷️ `Keyword`

Stores important terms for job scoring.

```python
id          UUID (auto)
word        CharField
weight      FloatField
```

### 💼 `Job`

Represents a job posting.

```python
id          UUID (auto)
title       CharField
description TextField
location    CharField
keywords    ManyToManyField(Keyword)
is_active   Boolean
```

### 👤 `Candidate`

Represents a job applicant.

```python
id          UUID (auto)
name        CharField
email       EmailField
phone       CharField
job         ForeignKey(Job)
score       FloatField
user        ForeignKey(User, optional)
```

### 📄 `Resume`

Stores uploaded resumes and extracted text.

```python
id            UUID (auto)
candidate     ForeignKey(Candidate)
file          FileField(upload_to='resumes/')
text_content  TextField (auto-filled)
size          Integer (file size in bytes)
file_type     CharField
uploaded_at   DateTime
```

---

## 🚀 API Endpoints

| Endpoint                  | Method | Description                     | Auth |
| ------------------------- | ------ | ------------------------------- | ---- |
| `/api/auth/token/`        | POST   | Get JWT token                   | ❌   |
| `/api/auth/refresh/`      | POST   | Refresh token                   | ❌   |
| `/api/cvs/jobs/`          | GET    | List all jobs                   | ❌   |
| `/api/cvs/jobs/create/`   | POST   | Create a job                    | ✅   |
| `/api/cvs/upload/`        | POST   | Upload a resume for scoring     | ✅   |
| `/api/cvs/my-candidates/` | GET    | List user’s uploaded candidates | ✅   |
| `/api/cvs/top/`           | GET    | Get top candidates by score     | ✅   |

---

## 🧮 Authentication

This API uses **JWT (JSON Web Tokens)** via `SimpleJWT`.

### Get a Token

```bash
POST /api/auth/token/
{
  "username": "admin",
  "password": "1234"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Use in Requests

```bash
Authorization: Bearer <access_token >
```

---

## 📦 Resume Upload Example

Endpoint:

```
POST /api/cvs/upload/
```

Body (FormData):

```
job_id: <UUID>
name: "John Doe"
email: "john@example.com"
phone: "0600000000"
file: <resume.pdf>
```

Response:

```json
{
  "candidate_id": "uuid",
  "score": 87.3,
  "job": "Backend Developer"
}
```

---

## 🧠 Scoring Logic

When a resume is uploaded:

1. Text is extracted from the file (via `parsing.py`)
2. Each keyword of the job is searched in the text ( via `scoring.py`)
3. Score is calculated as the **sum of weights of matched keywords**

---

## 🔐 CORS & Frontend Access

CORS is enabled in `settings.py` to allow requests from the React frontend.

```python
INSTALLED_APPS = [
    ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend URL
]
```

---

## 🧮 Useful Commands

```bash
python manage.py runserver        # Start dev server
python manage.py makemigrations   # Prepare DB migrations
python manage.py migrate          # Apply migrations
python manage.py createsuperuser  # Create admin user
```

---

## 🥪 Testing with cURL

```bash
curl -X POST http://127.0.0.1:8000/api/cvs/jobs/create/ \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"title":"Data Scientist","description":"AI stuff","location":"Paris" "keywords" : {

    }
}'
```

---

## 🧱 Future Improvements

Use of Machine learning for scoring purposes
Use of synonyms for keywords

- ***

## 👨‍💻 Author

**Eytahn Louis**\
📍 Europe\
🚀 Building modern AI-powered recruitment tools.

---

## 📜 License

MIT License © 2025 Eytahn Louis
