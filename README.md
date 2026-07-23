# ⚡ Production FastAPI Authentication & Showcase System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%20Async-red.svg)](https://www.sqlalchemy.org/)
[![Security](https://img.shields.io/badge/Auth-OAuth2%20%7C%20JWT%20%7C%20Bcrypt-purple.svg)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-grade, modular **FastAPI Authentication System** designed following standard Python project conventions. Features dual-token (Access + Refresh) OAuth2 JWT security, Passlib/Bcrypt password hashing, SQLAlchemy 2.0 Async ORM, pytest integration test coverage, and a glassmorphic dashboard interface engineered to showcase on LinkedIn.

---

## 🌟 Key Highlights

- **Standard Python Architecture**: Clean separation between `core`, `models`, `schemas`, `api/v1`, `templates`, and `tests`.
- **OAuth2 & JWT Auth Flow**: Fully compliant OAuth2 Bearer password flow with short-lived access tokens and refresh tokens.
- **Bcrypt Password Security**: One-way salt hashing using Passlib with strict validation.
- **Async SQLAlchemy 2.0 ORM**: Python `asyncio` event loop integration with SQLite (WAL mode) / PostgreSQL support.
- **Interactive Glassmorphic UI**: Built with Jinja2, modern CSS variables, live JWT Token Inspector, and interactive API tester.
- **Comprehensive Pytest Suite**: Async unit tests for registration, authentication, duplicate checks, and protected routes.
- **Deployment Ready**: Out-of-the-box `Dockerfile` and `render.yaml` for zero-configuration cloud hosting on Render or Railway.

---

## 🏗️ Project Architecture

```
FastApi-auth/
├── app/
│   ├── __init__.py
│   ├── main.py                  # App entrypoint, middleware & template routes
│   ├── core/
│   │   ├── config.py            # BaseSettings env manager (pydantic-settings)
│   │   ├── database.py          # Async SQLAlchemy engine & sessionmaker
│   │   └── security.py          # Password hashing & JWT generation/decoding
│   ├── models/
│   │   └── user.py              # SQLAlchemy User DB model
│   ├── schemas/
│   │   ├── token.py             # Token Pydantic schemas
│   │   └── user.py              # User Pydantic validation schemas
│   ├── api/
│   │   ├── deps.py              # Dependency injection (get_db, get_current_user)
│   │   └── v1/
│   │       ├── router.py        # Master API v1 router
│   │       └── endpoints/
│   │           ├── auth.py      # /signup, /login, /refresh, /me
│   │           └── dashboard.py # Protected showcase endpoints
│   ├── templates/               # Web UI Jinja2 templates
│   │   ├── base.html            # Base glassmorphic layout & header navigation
│   │   ├── index.html           # Landing page / showcase homepage
│   │   ├── login.html           # Sign In page
│   │   ├── register.html        # Registration page
│   │   ├── dashboard.html       # Interactive JWT token inspector & API playground
│   │   └── docs_guide.html      # Architectural blueprint guide
│   └── static/                  # Web UI Assets
│       ├── css/style.css        # Premium dark glassmorphism stylesheet
│       └── js/
│           ├── auth.js          # Client auth manager & token storage
│           └── dashboard.js     # Live token decoder & API tester logic
├── tests/                       # Pytest test suite
│   ├── conftest.py              # Async in-memory SQLite fixtures
│   ├── test_auth.py             # Auth flow integration tests
│   └── test_users.py            # Protected route tests
├── Dockerfile                   # Multi-stage production container configuration
├── render.yaml                  # One-click Render deployment manifest
├── pyproject.toml               # Modern Python project configuration
├── requirements.txt             # Pip dependency list
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/your-username/fastapi-auth-showcase.git
cd fastapi-auth-showcase

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

### 3. Launch Development Server

```bash
uvicorn app.main:app --reload
```

The application will start at `http://127.0.0.1:8000`.

- 🌐 **Web Dashboard UI**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📜 **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📘 **ReDoc API Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Automated Tests

Run the full pytest suite with async assertion logging:

```bash
pytest -v
```

---

## 📡 API Endpoint Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/signup` | Register a new user account | ❌ No |
| `POST` | `/api/v1/auth/login` | Authenticate user & return JWT tokens | ❌ No |
| `POST` | `/api/v1/auth/login-swagger` | OAuth2 password form login for Swagger UI | ❌ No |
| `POST` | `/api/v1/auth/refresh` | Obtain new access token via refresh token | ❌ No |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | 🔒 Yes (Bearer) |
| `POST` | `/api/v1/auth/logout` | Clear cookie session | ❌ No |
| `GET` | `/api/v1/dashboard/stats` | System statistics & server metrics | 🔒 Yes (Bearer) |
| `GET` | `/api/v1/dashboard/secret-payload` | Protected showcase data payload | 🔒 Yes (Bearer) |

---

## 🐳 Docker & Cloud Deployment

### Docker Container

```bash
# Build image
docker build -t fastapi-auth-showcase .

# Run container
docker run -p 8000:8000 fastapi-auth-showcase
```

### Render / Railway / Koyeb

1. Push your repository to GitHub.
2. Link your repo on [Render.com](https://render.com). Render will automatically detect `render.yaml` and configure Uvicorn automatically.
3. Share your live link on **LinkedIn** alongside your repository link!

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
