# -*- coding: utf-8 -*-
"""
Research Platform - Enterprise Edition
Main FastAPI Application
"""

import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app.models.user import User
from app.api.deps import get_current_user_optional, get_current_active_user
from app.services.permission import PermissionService
from app.services.document import DocumentService

# Import routers
from app.api.routers import auth, documents, workspaces, organizations, users, invites, notifications


# ============ Constants ============

# nginx proxy_redirect가 자동으로 / → /research/ 변환해주므로
# RedirectResponse에는 prefix 불필요
# 단, 템플릿/JS에서 브라우저가 직접 요청하는 URL에는 prefix 필요
PREFIX = "/research"


# ============ App Setup ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    Base.metadata.create_all(bind=engine)
    print(f"[*] Research Platform v{settings.APP_VERSION} starting...")
    print(f"[*] Data directory: {settings.DATA_DIR}")
    _create_initial_superuser()
    yield
    print("[*] Research Platform shutting down...")


def _create_initial_superuser():
    """Create initial superuser from environment."""
    from app.database import SessionLocal
    from app.services.security import SecurityService

    db = SessionLocal()
    try:
        existing_email = db.query(User).filter(User.email == settings.SUPERUSER_EMAIL).first()
        existing_username = db.query(User).filter(User.username == "admin").first()

        if not existing_email and not existing_username and settings.SUPERUSER_EMAIL and settings.SUPERUSER_PASSWORD:
            superuser = User(
                email=settings.SUPERUSER_EMAIL,
                username="admin",
                password_hash=SecurityService.hash_password(settings.SUPERUSER_PASSWORD),
                display_name="Administrator",
                is_superuser=True,
                is_active=True,
            )
            db.add(superuser)
            db.commit()
            print(f"[OK] Created superuser: {settings.SUPERUSER_EMAIL}")
    except Exception as e:
        print(f"[WARN] Could not create superuser: {e}")
        db.rollback()
    finally:
        db.close()


app = FastAPI(
    title="Research Platform",
    description="Enterprise Research Note Management Platform",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)


# ============ Middleware ============

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request."""
    request.state.request_id = str(uuid.uuid4())[:8]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


# ============ Static Files & Templates ============

STATIC_DIR = Path(__file__).parent.parent / "static_new"
TEMPLATES_DIR = Path(__file__).parent.parent / "templates_new"
NOTES_ROOT = Path(r"c:\Users\user\Desktop\Reseach_Note")

STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/notes", StaticFiles(directory=str(NOTES_ROOT)), name="notes")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 템플릿에서 {{ root_path }}/static/... 등 브라우저 URL용
templates.env.globals["root_path"] = PREFIX


# ============ API Routes ============

app.include_router(auth.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(workspaces.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(invites.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")


# ============ Web Routes ============
# ※ RedirectResponse는 prefix 없이!
#    nginx proxy_redirect / /research/ 가 자동 변환함
#    /login → Location: /research/login (브라우저에게)

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Landing page / Dashboard."""
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Login page."""
    if current_user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {
        "request": request,
    })


@app.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Registration page."""
    if current_user:
        return RedirectResponse(url="/")
    if not settings.ENABLE_REGISTRATION:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("register.html", {
        "request": request,
    })


@app.get("/workspaces/{workspace_id}", response_class=HTMLResponse)
async def workspace_page(
    workspace_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Workspace documents page."""
    from app.models.workspace import Workspace

    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if not PermissionService.check_permission(db, current_user.id, "read", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    return templates.TemplateResponse("workspace.html", {
        "request": request,
        "user": current_user,
        "workspace": workspace,
    })


@app.get("/documents/{document_id}", response_class=HTMLResponse)
async def document_view_page(
    document_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Document viewer page."""
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")

    DocumentService.record_view(db, document_id, current_user.id)
    is_favorited = DocumentService.is_favorited(db, current_user.id, document_id)
    can_edit = PermissionService.can_write(db, current_user.id, document)

    return templates.TemplateResponse("viewer.html", {
        "request": request,
        "user": current_user,
        "document": document,
        "is_favorited": is_favorited,
        "can_edit": can_edit,
    })


@app.get("/documents/{document_id}/edit", response_class=HTMLResponse)
async def document_edit_page(
    document_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Document editor page."""
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not PermissionService.can_write(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    return templates.TemplateResponse("editor.html", {
        "request": request,
        "user": current_user,
        "document": document,
    })


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """User settings page."""
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Admin dashboard (superuser only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/favorites", response_class=HTMLResponse)
async def favorites_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Favorites page."""
    return templates.TemplateResponse("favorites.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/search", response_class=HTMLResponse)
async def search_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Search page."""
    return templates.TemplateResponse("search.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/recent", response_class=HTMLResponse)
async def recent_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Recent documents page."""
    return templates.TemplateResponse("recent.html", {
        "request": request,
        "user": current_user,
    })


@app.get("/help", response_class=HTMLResponse)
async def help_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Help page with guides and shortcuts."""
    return templates.TemplateResponse("help.html", {
        "request": request,
        "user": current_user,
    })


# ============ Health Check ============

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }


# ============ Main Entry ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
    )
