# -*- coding: utf-8 -*-
"""
Users API Router
- Profile management
- User settings
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.security import SecurityService
from app.services.document import DocumentService
from app.services.audit import AuditService
from app.models.audit import AuditAction
from app.api.schemas import (
    UserResponse, UserUpdate, PasswordChange, 
    DocumentListItem, MessageResponse
)
from app.api.deps import get_current_active_user, get_current_superuser, get_client_ip


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        display_name=current_user.display_name,
        avatar_url=current_user.avatar_url,
        theme=current_user.theme,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at
    )


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    if data.display_name is not None:
        current_user.display_name = data.display_name
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url
    if data.bio is not None:
        current_user.bio = data.bio
    if data.theme is not None:
        current_user.theme = data.theme
    if data.locale is not None:
        current_user.locale = data.locale
    if data.timezone is not None:
        current_user.timezone = data.timezone
    
    db.commit()
    db.refresh(current_user)
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.USER_UPDATED,
        user_id=current_user.id,
        user_email=current_user.email,
        resource_type="user",
        resource_id=current_user.id,
    )
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        display_name=current_user.display_name,
        avatar_url=current_user.avatar_url,
        theme=current_user.theme,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at
    )


@router.post("/me/password", response_model=MessageResponse)
def change_password(
    request: Request,
    data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change current user's password."""
    # Verify current password
    if not SecurityService.verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    current_user.password_hash = SecurityService.hash_password(data.new_password)
    db.commit()
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.PASSWORD_CHANGED,
        user_id=current_user.id,
        user_email=current_user.email,
        ip_address=get_client_ip(request),
    )
    
    return MessageResponse(message="Password changed successfully")


@router.get("/me/recent", response_model=List[DocumentListItem])
def get_recent_documents(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get recently viewed documents."""
    documents = DocumentService.get_recent_documents(db, current_user.id, limit=limit)
    
    return [
        DocumentListItem(
            id=doc.id,
            title=doc.title,
            slug=doc.slug,
            icon=doc.icon,
            status=doc.status,
            owner_id=doc.owner_id,
            updated_at=doc.updated_at
        )
        for doc in documents
    ]


@router.get("/me/favorites", response_model=List[DocumentListItem])
def get_favorite_documents(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get favorite documents."""
    documents = DocumentService.get_favorites(db, current_user.id, limit=limit)
    
    return [
        DocumentListItem(
            id=doc.id,
            title=doc.title,
            slug=doc.slug,
            icon=doc.icon,
            status=doc.status,
            owner_id=doc.owner_id,
            updated_at=doc.updated_at
        )
        for doc in documents
    ]


@router.get("/me/stats")
def get_my_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for current user."""
    from app.models.document import Document, DocumentStatus
    from app.models.workspace import Workspace
    from app.models.content import Favorite
    from app.models.permission import RoleBinding
    from sqlalchemy import func
    
    # Count documents - for superuser count all, otherwise count owned
    if current_user.is_superuser:
        doc_count = db.query(func.count(Document.id)).filter(
            Document.status != DocumentStatus.DELETED
        ).scalar() or 0
    else:
        doc_count = db.query(func.count(Document.id)).filter(
            Document.owner_id == current_user.id,
            Document.status != DocumentStatus.DELETED
        ).scalar() or 0
    
    # Count workspaces user has access to
    workspace_count = db.query(func.count(RoleBinding.id)).filter(
        RoleBinding.user_id == current_user.id,
        RoleBinding.scope_type == 'workspace',
        RoleBinding.is_active == True
    ).scalar() or 0
    
    # If no workspace bindings, count all workspaces (for superuser)
    if workspace_count == 0 and current_user.is_superuser:
        workspace_count = db.query(func.count(Workspace.id)).scalar() or 0
    
    # Count favorites
    favorites_count = db.query(func.count(Favorite.id)).filter(
        Favorite.user_id == current_user.id
    ).scalar() or 0
    
    # Count collaborators (unique users in same workspaces)
    collaborators_count = 0
    if current_user.is_superuser:
        collaborators_count = db.query(func.count(User.id)).filter(
            User.is_active == True
        ).scalar() or 0
    
    return {
        "documents": doc_count,
        "workspaces": workspace_count,
        "favorites": favorites_count,
        "collaborators": collaborators_count
    }


@router.get("/me/activity")
def get_my_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get recent activity for the current user."""
    from app.models.audit import AuditLog
    
    # Get recent activities (visible actions like doc edits, comments, etc.)
    visible_actions = [
        'document_created', 'document_updated', 'document_deleted',
        'document_published', 'comment_created', 'workspace_created',
        'login'
    ]
    
    activities = db.query(AuditLog).filter(
        AuditLog.action.in_(visible_actions)
    ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    result = []
    for act in activities:
        # Get user display name
        user = db.query(User).filter(User.id == act.user_id).first() if act.user_id else None
        user_name = user.display_name if user else (act.user_email or "Unknown")
        
        # Determine activity type
        action_type = "edit"
        if "created" in act.action:
            action_type = "create"
        elif "deleted" in act.action:
            action_type = "delete"
        elif "comment" in act.action:
            action_type = "comment"
        elif "login" in act.action:
            action_type = "login"
        
        result.append({
            "id": act.id,
            "type": action_type,
            "action": act.action,
            "user": user_name,
            "user_id": act.user_id,
            "resource_type": act.resource_type,
            "resource_id": act.resource_id,
            "resource_name": act.resource_name,
            "timestamp": act.timestamp.isoformat() if act.timestamp else None,
        })
    
    return result


# ============ Admin endpoints ============

@router.get("", response_model=List[UserResponse])
def list_users(
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """List all users (admin only)."""
    query = db.query(User)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.email.ilike(search_term)) |
            (User.username.ilike(search_term)) |
            (User.display_name.ilike(search_term))
        )
    
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            display_name=u.display_name,
            avatar_url=u.avatar_url,
            theme=u.theme,
            is_superuser=u.is_superuser,
            created_at=u.created_at
        )
        for u in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        theme=user.theme,
        is_superuser=user.is_superuser,
        created_at=user.created_at
    )


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Soft delete
    user.is_active = False
    db.commit()
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.USER_DELETED,
        user_id=current_user.id,
        user_email=current_user.email,
        resource_type="user",
        resource_id=user_id,
        resource_name=user.email,
    )
    
    return MessageResponse(message="User deleted")


@router.get("/admin/stats")
def get_admin_stats(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics."""
    from app.models.organization import Organization
    from app.models.document import Document
    from app.models.workspace import Workspace
    
    total_users = db.query(User).filter(User.is_active == True).count()
    total_orgs = db.query(Organization).count()
    total_docs = db.query(Document).filter(Document.deleted_at == None).count()
    total_workspaces = db.query(Workspace).count()
    
    return {
        "total_users": total_users,
        "total_organizations": total_orgs,
        "total_documents": total_docs,
        "total_workspaces": total_workspaces
    }


@router.get("/admin/audit")
def get_audit_logs(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get audit logs for admin dashboard."""
    from app.models.audit import AuditLog
    
    logs = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            "user_email": log.user_email,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_name": log.resource_name,
            "ip_address": log.ip_address
        }
        for log in logs
    ]
