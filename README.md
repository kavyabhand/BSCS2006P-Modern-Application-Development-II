# Placement Portal Application

## Project Overview

This repository contains a project submitted as part of the IITM Online BS Degree Program in Data Science and Applications.

A Flask-based campus placement portal prototype with separate interfaces for Admin, Company, and Student roles. The backend exposes a REST API with JWT authentication, background jobs via Celery, and a Vue 3 frontend for the user interface.

## Features

- Admin login and dashboard
- Company registration, login, and dashboard
- Student registration, login, and dashboard
- Company approval workflow and placement drive management
- Student applications, resume uploads, and placement history
- Application status updates by companies
- CSV export of applications and admin reporting
- Optional email reminders via SMTP

## Tech stack

- Python 3
- Flask (REST API)
- Vue 3 + Vue Router + Vite (frontend)
- SQLite (via Flask-SQLAlchemy)
- Redis (caching and Celery broker)
- Celery (background tasks)
- Bootstrap 5, Axios

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- Redis installed (`brew install redis` on macOS)
- Recommended: create a virtual environment

## Install & Run

Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

Copy environment variables and set a secret key:

```bash
cp .env.example .env
```

Edit `.env` and set `SECRET_KEY`. SMTP settings are optional — the app runs without email configured.

Run the app (requires multiple terminals):

**Terminal 1 — Redis**
```bash
redis-server
```

**Terminal 2 — Flask backend**
```bash
cd backend
python app.py
```

**Terminal 3 — Celery worker**
```bash
cd backend
celery -A celery_worker.celery worker -l info
```

**Terminal 4 — Celery beat**
```bash
cd backend
celery -A celery_worker.celery beat -l info
```

**Terminal 5 — Vue frontend**
```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

The Flask API runs on **http://127.0.0.1:5000/** by default.

## Default admin login

| Email | Password |
|-------|----------|
| admin@placement.com | admin123 |

## Fresh database (before demo)

```bash
cd backend
rm -f placement.db instance/placement.db
```

Restart Flask — the default admin account is recreated automatically.

## Project structure

```
backend/
  app.py              — Flask application entrypoint
  config.py           — configuration and environment variables
  models.py           — SQLAlchemy data models
  extensions.py       — Flask extensions (db, jwt, cors, cache)
  mail.py             — SMTP email helpers
  celery_app.py       — Celery configuration
  celery_worker.py    — Celery worker entrypoint
  routes/
    auth.py           — login, register, logout
    admin.py          — admin dashboard and approvals
    company.py        — company drives and applications
    student.py        — student profile, drives, applications
  tasks/
    export.py         — CSV export jobs
    reports.py        — admin report generation
    reminders.py         — email and webhook reminders

frontend/
  src/
    pages/            — Vue page components (admin, company, student views)
    router/index.js   — frontend routing
    services/api.js   — Axios API client
  index.html          — frontend entrypoint
```

Key frontend pages:

- `src/pages/Home.vue` — landing page
- `src/pages/Login.vue`, `src/pages/Register.vue`
- `src/pages/AdminDashboard.vue`, `src/pages/PendingCompanies.vue`, `src/pages/PendingDrives.vue`
- `src/pages/CompanyDashboard.vue`, `src/pages/CompanyDrives.vue`, `src/pages/CompanyApplications.vue`
- `src/pages/StudentDashboard.vue`, `src/pages/StudentDrives.vue`, `src/pages/StudentApplications.vue`
