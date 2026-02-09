# -*- coding: utf-8 -*-
"""
Invites API Router
- Create invite codes
- Accept invites
- List invites
"""

from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.models.notification import Invite, InviteStatus, Notification, NotificationType
from app.models.permission import RoleBinding, ScopeType, RoleType
from app.services.permission import PermissionService
from app.api.deps import get_current_active_user


router = APIRouter(prefix="/invites", tags=["Invites"])


class InviteCreate(BaseModel):
    workspace_id: str
    role: str = "viewer"
    max_uses: int = 1
    expires_in_days: int = 7


class InviteResponse(BaseModel):
    id: str
    code: str
    workspace_id: str
    workspace_name: str = ""
    role: str
    status: str
    max_uses: int
    use_count: int
    created_at: datetime
    expires_at: datetime | None


@router.post("", response_model=InviteResponse)
def create_invite(
    data: InviteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create an invite code for a workspace."""
    # Check permission
    if not PermissionService.can_manage_workspace(db, current_user.id, data.workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    workspace = db.query(Workspace).filter(Workspace.id == data.workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    invite = Invite(
        code=Invite.generate_code(),
        workspace_id=data.workspace_id,
        created_by_id=current_user.id,
        role=data.role,
        max_uses=data.max_uses,
        expires_at=datetime.utcnow() + timedelta(days=data.expires_in_days)
    )
    
    db.add(invite)
    db.commit()
    db.refresh(invite)
    
    return InviteResponse(
        id=invite.id,
        code=invite.code,
        workspace_id=invite.workspace_id,
        workspace_name=workspace.name,
        role=invite.role,
        status=invite.status,
        max_uses=invite.max_uses,
        use_count=invite.use_count,
        created_at=invite.created_at,
        expires_at=invite.expires_at
    )


@router.get("/workspace/{workspace_id}", response_model=List[InviteResponse])
def list_workspace_invites(
    workspace_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all invites for a workspace."""
    if not PermissionService.can_manage_workspace(db, current_user.id, workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    invites = db.query(Invite).filter(
        Invite.workspace_id == workspace_id,
        Invite.status == InviteStatus.PENDING.value
    ).all()
    
    return [
        InviteResponse(
            id=inv.id,
            code=inv.code,
            workspace_id=inv.workspace_id,
            workspace_name=workspace.name if workspace else "",
            role=inv.role,
            status=inv.status,
            max_uses=inv.max_uses,
            use_count=inv.use_count,
            created_at=inv.created_at,
            expires_at=inv.expires_at
        )
        for inv in invites
    ]


@router.post("/accept/{code}")
def accept_invite(
    code: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Accept an invite code to join a workspace."""
    invite = db.query(Invite).filter(Invite.code == code.upper()).first()
    
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    if not invite.is_valid:
        raise HTTPException(status_code=400, detail="Invite is no longer valid")
    
    # Check if already a member
    existing = db.query(RoleBinding).filter(
        RoleBinding.user_id == current_user.id,
        RoleBinding.workspace_id == invite.workspace_id,
        RoleBinding.scope_type == ScopeType.WORKSPACE.value,
        RoleBinding.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already a member of this workspace")
    
    # Grant role
    PermissionService.grant_role(
        db,
        user_id=current_user.id,
        role=invite.role,
        scope_type=ScopeType.WORKSPACE,
        scope_id=invite.workspace_id,
        granted_by_id=invite.created_by_id
    )
    
    # Update invite
    invite.use_count += 1
    invite.accepted_by_id = current_user.id
    invite.accepted_at = datetime.utcnow()
    
    if invite.max_uses > 0 and invite.use_count >= invite.max_uses:
        invite.status = InviteStatus.ACCEPTED.value
    
    # Get workspace for notification
    workspace = db.query(Workspace).filter(Workspace.id == invite.workspace_id).first()
    
    # Create notification for creator
    notification = Notification(
        user_id=invite.created_by_id,
        type=NotificationType.INVITE.value,
        title="초대가 수락되었습니다",
        message=f"{current_user.display_name}님이 {workspace.name} 워크스페이스에 참여했습니다.",
        link=f"/workspaces/{invite.workspace_id}",
        workspace_id=invite.workspace_id,
        from_user_id=current_user.id
    )
    db.add(notification)
    
    db.commit()
    
    return {"message": f"Successfully joined workspace: {workspace.name}", "workspace_id": workspace.id}


@router.delete("/{invite_id}")
def revoke_invite(
    invite_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Revoke an invite."""
    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    if not PermissionService.can_manage_workspace(db, current_user.id, invite.workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    invite.status = InviteStatus.REVOKED.value
    db.commit()
    
    return {"message": "Invite revoked"}
