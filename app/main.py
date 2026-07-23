from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib

from app.api.deps import extract_token_from_request
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import init_db
from app.core.security import decode_jwt_token

BASE_DIR = pathlib.Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application Lifespan Context Manager.
    Initializes database tables on application startup.
    """
    # Startup: Initialize DB tables
    await init_db()
    yield
    # Shutdown logic (if any)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Setup CORS Middleware
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

_db_initialized = False

@app.middleware("http")
async def ensure_db_initialized(request: Request, call_next):
    global _db_initialized
    if not _db_initialized:
        await init_db()
        _db_initialized = True
    return await call_next(request)

# Mount Static Files & Jinja2 Templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Helper function to get current user info for Jinja2 template rendering
def get_user_from_cookies(request: Request):
    token = request.cookies.get("access_token")
    if token:
        if token.startswith("Bearer "):
            token = token[7:]
        try:
            payload = decode_jwt_token(token)
            return {"id": payload.get("sub")}
        except Exception:
            return None
    return None


# --------------------------------------------------------------------------
# Web UI Page Routes (Jinja2 Templates)
# --------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    user = get_user_from_cookies(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_user_from_cookies(request)
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user = get_user_from_cookies(request)
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("register.html", {"request": request, "user": None})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    user = get_user_from_cookies(request)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@app.get("/guide", response_class=HTMLResponse)
async def guide_page(request: Request):
    user = get_user_from_cookies(request)
    return templates.TemplateResponse("docs_guide.html", {"request": request, "user": user})


@app.get("/health")
async def health_check():
    """Application Health Check Endpoint."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
