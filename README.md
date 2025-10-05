# 🧠 ATS Project — Applicant Tracking System

A modern lightweight **ATS (Applicant Tracking System)** built with **Django REST Framework** & **React**.  
Companies can post jobs, candidates can upload resumes, and the system automatically scores CVs based on job keywords.

---

## 🚀 Features
- Job posting & management  
- Resume upload & scoring  
- Candidate ranking by score  
- JWT authentication  
- Admin & user dashboards  
- Filtering by keywords and location  

---

## 🧩 Tech Stack
**Backend:** Django REST Framework, django-filter, drf-yasg, JWT  
**Frontend:** React (Vite), Axios, React Router  
**Database:** SQLite (dev) → PostgreSQL (prod ready)

---

## ⚙️ Installation

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # mac/linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
