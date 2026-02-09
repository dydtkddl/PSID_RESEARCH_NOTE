# -*- coding: utf-8 -*-
"""
Workspaces API Router
- Workspace management
- Member management
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.workspace import Workspace, Project
from app.models.organization import Organization
from app.models.permission import RoleBinding, ScopeType, RoleType
from app.services.permission import PermissionService
from app.services.security import SecurityService
from app.services.audit import AuditService
from app.models.audit import AuditAction
from app.api.schemas import (
    WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse,
    RoleBindingCreate, RoleBindingResponse, MessageResponse
)
from app.api.deps import get_current_active_user


router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(
    org_id: str,
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new workspace in an organization."""
    # Check org permission
    if not PermissionService.check_permission(db, current_user.id, "write", "organization", org_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Check org exists
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    workspace = Workspace(
        org_id=org_id,
        name=data.name,
        slug=SecurityService.generate_slug(data.name),
        description=data.description,
        icon=data.icon,
    )
    
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    
    # Grant creator owner role
    PermissionService.grant_role(
        db,
        user_id=current_user.id,
        role=RoleType.OWNER.value,
        scope_type=ScopeType.WORKSPACE,
        scope_id=workspace.id,
        granted_by_id=current_user.id
    )
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.WORKSPACE_CREATED,
        user_id=current_user.id,
        user_email=current_user.email,
        org_id=org_id,
        workspace_id=workspace.id,
        resource_type="workspace",
        resource_id=workspace.id,
        resource_name=workspace.name,
    )
    
    return WorkspaceResponse(
        id=workspace.id,
        org_id=workspace.org_id,
        name=workspace.name,
        slug=workspace.slug,
        description=workspace.description,
        icon=workspace.icon,
        is_default=workspace.is_default,
        created_at=workspace.created_at
    )


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get workspace by ID."""
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.is_active == True
    ).first()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Check permission
    if not PermissionService.check_permission(db, current_user.id, "read", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return WorkspaceResponse(
        id=workspace.id,
        org_id=workspace.org_id,
        name=workspace.name,
        slug=workspace.slug,
        description=workspace.description,
        icon=workspace.icon,
        is_default=workspace.is_default,
        created_at=workspace.created_at
    )


@router.get("", response_model=List[WorkspaceResponse])
def list_workspaces(
    org_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List workspaces in an organization that user can access."""
    workspace_ids = PermissionService.get_accessible_workspaces(db, current_user.id, org_id)
    
    if not workspace_ids:
        return []
    
    workspaces = db.query(Workspace).filter(
        Workspace.id.in_(workspace_ids),
        Workspace.is_active == True
    ).order_by(Workspace.name).all()
    
    return [
        WorkspaceResponse(
            id=ws.id,
            org_id=ws.org_id,
            name=ws.name,
            slug=ws.slug,
            description=ws.description,
            icon=ws.icon,
            is_default=ws.is_default,
            created_at=ws.created_at
        )
        for ws in workspaces
    ]


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(
    workspace_id: str,
    data: WorkspaceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update workspace settings."""
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Check permission
    if not PermissionService.can_manage_workspace(db, current_user.id, workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if data.name:
        workspace.name = data.name
        workspace.slug = SecurityService.generate_slug(data.name)
    if data.description is not None:
        workspace.description = data.description
    if data.icon:
        workspace.icon = data.icon
    if data.default_visibility:
        workspace.default_visibility = data.default_visibility
    
    db.commit()
    db.refresh(workspace)
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.WORKSPACE_UPDATED,
        user_id=current_user.id,
        user_email=current_user.email,
        org_id=workspace.org_id,
        workspace_id=workspace.id,
        resource_type="workspace",
        resource_id=workspace.id,
        resource_name=workspace.name,
    )
    
    return WorkspaceResponse(
        id=workspace.id,
        org_id=workspace.org_id,
        name=workspace.name,
        slug=workspace.slug,
        description=workspace.description,
        icon=workspace.icon,
        is_default=workspace.is_default,
        created_at=workspace.created_at
    )


@router.delete("/{workspace_id}", response_model=MessageResponse)
def delete_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a workspace (soft delete)."""
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Check permission - only owner can delete
    role = PermissionService.get_user_role_for_scope(
        db, current_user.id, ScopeType.WORKSPACE, workspace_id
    )
    
    if role != RoleType.OWNER.value and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only owner can delete workspace")
    
    workspace.is_active = False
    db.commit()
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.WORKSPACE_DELETED,
        user_id=current_user.id,
        user_email=current_user.email,
        org_id=workspace.org_id,
        workspace_id=workspace.id,
        resource_type="workspace",
        resource_id=workspace.id,
        resource_name=workspace.name,
    )
    
    return MessageResponse(message="Workspace deleted")


@router.post("/reorder", response_model=MessageResponse)
def reorder_workspaces(
    workspace_ids: List[str],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reorder workspaces by updating their positions."""
    for idx, ws_id in enumerate(workspace_ids):
        workspace = db.query(Workspace).filter(Workspace.id == ws_id).first()
        if workspace:
            workspace.position = idx
    
    db.commit()
    return MessageResponse(message="Workspaces reordered")


# ============ Members ============

@router.get("/{workspace_id}/members", response_model=List[RoleBindingResponse])
def list_workspace_members(
    workspace_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List workspace members and their roles."""
    # Check permission
    if not PermissionService.check_permission(db, current_user.id, "read", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    bindings = db.query(RoleBinding).filter(
        RoleBinding.workspace_id == workspace_id,
        RoleBinding.scope_type == ScopeType.WORKSPACE.value,
        RoleBinding.is_active == True
    ).all()
    
    result = []
    for binding in bindings:
        user = db.query(User).filter(User.id == binding.user_id).first()
        result.append(RoleBindingResponse(
            id=binding.id,
            user_id=binding.user_id,
            user_email=user.email if user else None,
            role=binding.role,
            scope_type=binding.scope_type,
            scope_id=binding.workspace_id,
            is_active=binding.is_active,
            created_at=binding.created_at,
            expires_at=binding.expires_at
        ))
    
    return result


@router.post("/{workspace_id}/members", response_model=RoleBindingResponse, status_code=status.HTTP_201_CREATED)
def add_workspace_member(
    workspace_id: str,
    user_id: str,
    role: str = Query(..., description="Role to assign"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a member to workspace with specified role."""
    # Check permission
    if not PermissionService.check_permission(db, current_user.id, "manage_members", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Validate role
    try:
        RoleType(role)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
    
    # Check user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already member
    existing = db.query(RoleBinding).filter(
        RoleBinding.user_id == user_id,
        RoleBinding.workspace_id == workspace_id,
        RoleBinding.scope_type == ScopeType.WORKSPACE.value,
        RoleBinding.is_active == True
    ).first()
    
    if existing:
        # Update role
        existing.role = role
        db.commit()
        binding = existing
    else:
        binding = PermissionService.grant_role(
            db,
            user_id=user_id,
            role=role,
            scope_type=ScopeType.WORKSPACE,
            scope_id=workspace_id,
            granted_by_id=current_user.id
        )
    
    # Audit
    AuditService.log_permission_change(
        db,
        action=AuditAction.ROLE_ASSIGNED,
        target_user_id=user_id,
        target_user_email=user.email,
        changed_by_id=current_user.id,
        changed_by_email=current_user.email,
        scope_type="workspace",
        scope_id=workspace_id,
        new_role=role,
    )
    
    return RoleBindingResponse(
        id=binding.id,
        user_id=binding.user_id,
        user_email=user.email,
        role=binding.role,
        scope_type=binding.scope_type,
        scope_id=binding.workspace_id,
        is_active=binding.is_active,
        created_at=binding.created_at,
        expires_at=binding.expires_at
    )


@router.delete("/{workspace_id}/members/{user_id}", response_model=MessageResponse)
def remove_workspace_member(
    workspace_id: str,
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a member from workspace."""
    # Check permission
    if not PermissionService.check_permission(db, current_user.id, "manage_members", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Can't remove yourself if you're the only owner
    if user_id == current_user.id:
        owner_count = db.query(RoleBinding).filter(
            RoleBinding.workspace_id == workspace_id,
            RoleBinding.role == RoleType.OWNER.value,
            RoleBinding.is_active == True
        ).count()
        
        if owner_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the only owner")
    
    # Get user email for audit
    user = db.query(User).filter(User.id == user_id).first()
    
    success = PermissionService.revoke_role(db, user_id, ScopeType.WORKSPACE, workspace_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Audit
    if user:
        AuditService.log_permission_change(
            db,
            action=AuditAction.ROLE_REMOVED,
            target_user_id=user_id,
            target_user_email=user.email,
            changed_by_id=current_user.id,
            changed_by_email=current_user.email,
            scope_type="workspace",
            scope_id=workspace_id,
        )
    
    return MessageResponse(message="Member removed from workspace")
