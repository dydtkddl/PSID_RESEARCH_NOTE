# -*- coding: utf-8 -*-
"""
API Schemas (Pydantic models)
- Request/Response validation
- Data transfer objects
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


# ============ Auth Schemas ============

class LoginRequest(BaseModel):
    """Login request payload."""
    email_or_username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class UserResponse(BaseModel):
    """User information response."""
    id: str
    email: str
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    theme: str
    is_superuser: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Full login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ============ User Schemas ============

class UserCreate(BaseModel):
    """User creation payload."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    """User update payload."""
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    theme: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None


class PasswordChange(BaseModel):
    """Password change request."""
    current_password: str
    new_password: str = Field(..., min_length=8)


# ============ Organization Schemas ============

class OrganizationCreate(BaseModel):
    """Organization creation payload."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Organization update payload."""
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    default_theme: Optional[str] = None


class OrganizationResponse(BaseModel):
    """Organization response."""
    id: str
    name: str
    slug: str
    description: Optional[str]
    logo_url: Optional[str]
    primary_color: str
    owner_id: str
    plan: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Workspace Schemas ============

class WorkspaceCreate(BaseModel):
    """Workspace creation payload."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    icon: str = "📁"


class WorkspaceUpdate(BaseModel):
    """Workspace update payload."""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    default_visibility: Optional[str] = None


class WorkspaceResponse(BaseModel):
    """Workspace response."""
    id: str
    org_id: str
    name: str
    slug: str
    description: Optional[str]
    icon: str
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Document Schemas ============

class DocumentCreate(BaseModel):
    """Document creation payload."""
    title: str = Field(..., min_length=1, max_length=500)
    content: str = ""
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    parent_id: Optional[str] = None
    visibility: str = "workspace"
    metadata: Optional[Dict[str, Any]] = None


class DocumentUpdate(BaseModel):
    """Document update payload."""
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    change_summary: Optional[str] = None


class DocumentResponse(BaseModel):
    """Document response."""
    id: str
    workspace_id: str
    project_id: Optional[str]
    parent_id: Optional[str]
    title: str
    slug: str
    content: str
    content_html: Optional[str]
    summary: Optional[str]
    icon: str
    metadata: Dict[str, Any]
    status: str
    visibility: str
    owner_id: str
    current_version: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    is_favorited: bool = False
    
    class Config:
        from_attributes = True


class DocumentListItem(BaseModel):
    """Document list item (summary)."""
    id: str
    title: str
    slug: str
    icon: str
    status: str
    owner_id: str
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Paginated document list."""
    items: List[DocumentListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class DocumentVersionResponse(BaseModel):
    """Document version response."""
    id: str
    document_id: str
    version_number: int
    title: str
    content: str
    author_id: Optional[str]
    change_summary: Optional[str]
    word_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Comment Schemas ============

class CommentCreate(BaseModel):
    """Comment creation payload."""
    content: str = Field(..., min_length=1)
    parent_id: Optional[str] = None
    anchor_start: Optional[int] = None
    anchor_end: Optional[int] = None
    anchor_text: Optional[str] = None


class CommentUpdate(BaseModel):
    """Comment update payload."""
    content: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    """Comment response."""
    id: str
    document_id: str
    parent_id: Optional[str]
    author_id: str
    author_name: Optional[str] = None
    content: str
    anchor_text: Optional[str] = None
    is_resolved: bool
    created_at: datetime
    updated_at: datetime
    replies: List["CommentResponse"] = []
    
    class Config:
        from_attributes = True


CommentResponse.model_rebuild()


# ============ Highlight Schemas ============

class HighlightCreate(BaseModel):
    """Highlight creation payload."""
    start_offset: int
    end_offset: int
    text: str
    note: Optional[str] = None
    color: str = "#fff59d"
    content_hash: Optional[str] = None


class HighlightUpdate(BaseModel):
    """Highlight update payload."""
    note: Optional[str] = None
    color: Optional[str] = None


class HighlightResponse(BaseModel):
    """Highlight response."""
    id: str
    document_id: str
    user_id: str
    start_offset: int
    end_offset: int
    text: str
    note: Optional[str]
    color: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Permission Schemas ============

class RoleBindingCreate(BaseModel):
    """Role binding creation payload."""
    user_id: str
    role: str
    scope_type: str
    scope_id: str
    expires_at: Optional[datetime] = None


class RoleBindingResponse(BaseModel):
    """Role binding response."""
    id: str
    user_id: str
    user_email: Optional[str] = None
    role: str
    scope_type: str
    scope_id: Optional[str]
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PermissionCheck(BaseModel):
    """Permission check request."""
    permission: str
    resource_type: str
    resource_id: str


class PermissionCheckResponse(BaseModel):
    """Permission check response."""
    allowed: bool
    role: Optional[str] = None


# ============ Audit Schemas ============

class AuditLogResponse(BaseModel):
    """Audit log response."""
    id: str
    timestamp: datetime
    user_id: Optional[str]
    user_email: Optional[str]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    resource_name: Optional[str]
    details: Dict[str, Any]
    ip_address: Optional[str]
    success: bool
    
    class Config:
        from_attributes = True


class AuditLogList(BaseModel):
    """Audit log list."""
    items: List[AuditLogResponse]
    total: int


# ============ Search Schemas ============

class SearchRequest(BaseModel):
    """Search request."""
    query: str = Field(..., min_length=1)
    workspace_id: Optional[str] = None
    document_type: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    page: int = 1
    page_size: int = 20


class SearchResult(BaseModel):
    """Search result item."""
    id: str
    title: str
    snippet: str
    type: str
    workspace_id: str
    workspace_name: str
    updated_at: datetime
    score: float


class SearchResponse(BaseModel):
    """Search response."""
    items: List[SearchResult]
    total: int
    query: str
    page: int
    page_size: int


# ============ Common Schemas ============

class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
