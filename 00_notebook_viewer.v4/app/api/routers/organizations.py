# -*- coding: utf-8 -*-
"""
Organizations API Router
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.workspace import Workspace
from app.models.permission import RoleBinding, ScopeType, RoleType
from app.services.permission import PermissionService
from app.services.security import SecurityService
from app.services.audit import AuditService
from app.models.audit import AuditAction
from app.api.schemas import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse,
    WorkspaceResponse, MessageResponse
)
from app.api.deps import get_current_active_user


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    data: OrganizationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new organization."""
    org = Organization(
        name=data.name,
        slug=SecurityService.generate_slug(data.name),
        description=data.description,
        owner_id=current_user.id,
    )
    
    db.add(org)
    db.commit()
    db.refresh(org)
    
    # Grant creator owner role
    PermissionService.grant_role(
        db,
        user_id=current_user.id,
        role=RoleType.OWNER.value,
        scope_type=ScopeType.ORGANIZATION,
        scope_id=org.id,
        granted_by_id=current_user.id
    )
    
    # Create default workspace
    default_ws = Workspace(
        org_id=org.id,
        name="General",
        slug="general",
        description="Default workspace",
        icon="🏠",
        is_default=True,
    )
    db.add(default_ws)
    db.commit()
    
    # Grant owner role on default workspace too
    PermissionService.grant_role(
        db,
        user_id=current_user.id,
        role=RoleType.OWNER.value,
        scope_type=ScopeType.WORKSPACE,
        scope_id=default_ws.id,
        granted_by_id=current_user.id
    )
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.ORG_CREATED,
        user_id=current_user.id,
        user_email=current_user.email,
        org_id=org.id,
        resource_type="organization",
        resource_id=org.id,
        resource_name=org.name,
    )
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        description=org.description,
        logo_url=org.logo_url,
        primary_color=org.primary_color,
        owner_id=org.owner_id,
        plan=org.plan,
        created_at=org.created_at
    )


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(
    org_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get organization by ID."""
    org = db.query(Organization).filter(
        Organization.id == org_id,
        Organization.is_active == True
    ).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if user has any access to this org
    role = PermissionService.get_user_role_for_scope(
        db, current_user.id, ScopeType.ORGANIZATION, org_id
    )
    
    if not role and not current_user.is_superuser:
        # Check if user has access to any workspace in org
        accessible_ws = PermissionService.get_accessible_workspaces(db, current_user.id, org_id)
        if not accessible_ws:
            raise HTTPException(status_code=403, detail="Permission denied")
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        description=org.description,
        logo_url=org.logo_url,
        primary_color=org.primary_color,
        owner_id=org.owner_id,
        plan=org.plan,
        created_at=org.created_at
    )


@router.get("", response_model=List[OrganizationResponse])
def list_organizations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List organizations the current user has access to."""
    # Get orgs where user has a role binding
    bindings = db.query(RoleBinding).filter(
        RoleBinding.user_id == current_user.id,
        RoleBinding.scope_type == ScopeType.ORGANIZATION.value,
        RoleBinding.is_active == True
    ).all()
    
    org_ids = [b.org_id for b in bindings if b.org_id]
    
    # Also include orgs where user has workspace-level access
    ws_bindings = db.query(RoleBinding).filter(
        RoleBinding.user_id == current_user.id,
        RoleBinding.scope_type == ScopeType.WORKSPACE.value,
        RoleBinding.is_active == True
    ).all()
    
    for b in ws_bindings:
        if b.workspace_id:
            ws = db.query(Workspace).filter(Workspace.id == b.workspace_id).first()
            if ws and ws.org_id not in org_ids:
                org_ids.append(ws.org_id)
    
    if not org_ids:
        return []
    
    orgs = db.query(Organization).filter(
        Organization.id.in_(org_ids),
        Organization.is_active == True
    ).order_by(Organization.name).all()
    
    return [
        OrganizationResponse(
            id=org.id,
            name=org.name,
            slug=org.slug,
            description=org.description,
            logo_url=org.logo_url,
            primary_color=org.primary_color,
            owner_id=org.owner_id,
            plan=org.plan,
            created_at=org.created_at
        )
        for org in orgs
    ]


@router.put("/{org_id}", response_model=OrganizationResponse)
def update_organization(
    org_id: str,
    data: OrganizationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update organization settings."""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check permission
    if not PermissionService.check_permission(db, current_user.id, "manage_settings", "organization", org_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if data.name:
        org.name = data.name
        org.slug = SecurityService.generate_slug(data.name)
    if data.description is not None:
        org.description = data.description
    if data.logo_url is not None:
        org.logo_url = data.logo_url
    if data.primary_color:
        org.primary_color = data.primary_color
    if data.default_theme:
        org.default_theme = data.default_theme
    
    db.commit()
    db.refresh(org)
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.ORG_UPDATED,
        user_id=current_user.id,
        user_email=current_user.email,
        org_id=org.id,
        resource_type="organization",
        resource_id=org.id,
        resource_name=org.name,
    )
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        description=org.description,
        logo_url=org.logo_url,
        primary_color=org.primary_color,
        owner_id=org.owner_id,
        plan=org.plan,
        created_at=org.created_at
    )


@router.get("/{org_id}/workspaces", response_model=List[WorkspaceResponse])
def list_org_workspaces(
    org_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all workspaces in an organization that user can access."""
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
