# -*- coding: utf-8 -*-
"""
Permission Service
- RBAC evaluation
- Permission checking
- Role resolution with precedence
"""

from typing import Optional, List, Dict, Set
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.permission import (
    RoleBinding, Permission, Role, 
    RoleType, ScopeType, ROLE_PERMISSIONS
)
from app.models.user import User
from app.models.document import Document
from app.models.workspace import Workspace, Project
from app.models.organization import Organization


class PermissionService:
    """
    RBAC Permission evaluation service.
    
    Precedence order (highest to lowest):
    1. Document-level override
    2. Project-level override  
    3. Workspace-level role
    4. Organization-level role
    5. System superuser
    """
    
    @classmethod
    def get_role_permissions(cls, role_name: str) -> Dict[str, bool]:
        """Get default permissions for a role."""
        try:
            role_type = RoleType(role_name)
            return ROLE_PERMISSIONS.get(role_type, {}).copy()
        except ValueError:
            # Custom role - would need to look up from database
            return {}
    
    @classmethod
    def get_user_role_for_scope(
        cls,
        db: Session,
        user_id: str,
        scope_type: ScopeType,
        scope_id: str
    ) -> Optional[str]:
        """Get user's role for a specific scope."""
        now = datetime.utcnow()
        
        # Build query based on scope type
        query = db.query(RoleBinding).filter(
            RoleBinding.user_id == user_id,
            RoleBinding.scope_type == scope_type.value,
            RoleBinding.is_active == True,
            or_(
                RoleBinding.expires_at == None,
                RoleBinding.expires_at > now
            )
        )
        
        if scope_type == ScopeType.ORGANIZATION:
            query = query.filter(RoleBinding.org_id == scope_id)
        elif scope_type == ScopeType.WORKSPACE:
            query = query.filter(RoleBinding.workspace_id == scope_id)
        elif scope_type == ScopeType.PROJECT:
            query = query.filter(RoleBinding.project_id == scope_id)
        elif scope_type == ScopeType.DOCUMENT:
            query = query.filter(RoleBinding.document_id == scope_id)
        
        binding = query.first()
        return binding.role if binding else None
    
    @classmethod
    def get_effective_role_for_document(
        cls,
        db: Session,
        user_id: str,
        document: Document
    ) -> Optional[str]:
        """
        Get user's effective role for a document.
        Applies precedence: doc > project > workspace > org
        """
        # Check superuser
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.is_superuser:
            return RoleType.OWNER.value
        
        # 1. Document-level override
        doc_role = cls.get_user_role_for_scope(
            db, user_id, ScopeType.DOCUMENT, document.id
        )
        if doc_role:
            return doc_role
        
        # 2. Project-level override (if document has a project)
        if document.project_id:
            project_role = cls.get_user_role_for_scope(
                db, user_id, ScopeType.PROJECT, document.project_id
            )
            if project_role:
                return project_role
        
        # 3. Workspace-level role
        workspace_role = cls.get_user_role_for_scope(
            db, user_id, ScopeType.WORKSPACE, document.workspace_id
        )
        if workspace_role:
            return workspace_role
        
        # 4. Organization-level role
        workspace = db.query(Workspace).filter(
            Workspace.id == document.workspace_id
        ).first()
        
        if workspace:
            org_role = cls.get_user_role_for_scope(
                db, user_id, ScopeType.ORGANIZATION, workspace.org_id
            )
            if org_role:
                return org_role
        
        return None
    
    @classmethod
    def check_permission(
        cls,
        db: Session,
        user_id: str,
        permission: str,
        resource_type: str,
        resource_id: str
    ) -> bool:
        """
        Check if user has specific permission on a resource.
        """
        # Check superuser
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.is_superuser:
            return True
        
        # Check fine-grained permission override first
        perm_override = db.query(Permission).filter(
            Permission.user_id == user_id,
            Permission.resource_type == resource_type,
            Permission.resource_id == resource_id,
            Permission.permission == permission
        ).first()
        
        if perm_override:
            return perm_override.allowed
        
        # Get effective role and check role permissions
        if resource_type == "document":
            document = db.query(Document).filter(Document.id == resource_id).first()
            if not document:
                return False
            
            role = cls.get_effective_role_for_document(db, user_id, document)
            if not role:
                return False
            
            role_perms = cls.get_role_permissions(role)
            return role_perms.get(permission, False)
        
        elif resource_type == "workspace":
            workspace = db.query(Workspace).filter(Workspace.id == resource_id).first()
            if not workspace:
                return False
            
            # Check workspace role
            ws_role = cls.get_user_role_for_scope(
                db, user_id, ScopeType.WORKSPACE, resource_id
            )
            if ws_role:
                return cls.get_role_permissions(ws_role).get(permission, False)
            
            # Fallback to org role
            org_role = cls.get_user_role_for_scope(
                db, user_id, ScopeType.ORGANIZATION, workspace.org_id
            )
            if org_role:
                return cls.get_role_permissions(org_role).get(permission, False)
            
            return False
        
        elif resource_type == "organization":
            org_role = cls.get_user_role_for_scope(
                db, user_id, ScopeType.ORGANIZATION, resource_id
            )
            if org_role:
                return cls.get_role_permissions(org_role).get(permission, False)
            return False
        
        return False
    
    @classmethod
    def can_read(cls, db: Session, user_id: str, document: Document) -> bool:
        """Check if user can read a document."""
        # Owner always can read
        if document.owner_id == user_id:
            return True
        
        return cls.check_permission(db, user_id, "read", "document", document.id)
    
    @classmethod
    def can_write(cls, db: Session, user_id: str, document: Document) -> bool:
        """Check if user can edit a document."""
        # Owner always can write
        if document.owner_id == user_id:
            return True
        
        return cls.check_permission(db, user_id, "write", "document", document.id)
    
    @classmethod
    def can_delete(cls, db: Session, user_id: str, document: Document) -> bool:
        """Check if user can delete a document."""
        # Owner always can delete
        if document.owner_id == user_id:
            return True
        
        return cls.check_permission(db, user_id, "delete", "document", document.id)
    
    @classmethod
    def can_manage_workspace(cls, db: Session, user_id: str, workspace_id: str) -> bool:
        """Check if user can manage workspace settings."""
        return cls.check_permission(db, user_id, "manage_settings", "workspace", workspace_id)
    
    @classmethod
    def get_accessible_workspaces(cls, db: Session, user_id: str, org_id: str) -> List[str]:
        """Get list of workspace IDs user can access in an organization."""
        now = datetime.utcnow()
        
        # Check if user has org-level role
        org_role = cls.get_user_role_for_scope(db, user_id, ScopeType.ORGANIZATION, org_id)
        
        if org_role:
            # User has org-level access - can see all workspaces
            workspaces = db.query(Workspace.id).filter(
                Workspace.org_id == org_id,
                Workspace.is_active == True
            ).all()
            return [ws.id for ws in workspaces]
        
        # Otherwise, only workspaces with explicit bindings
        bindings = db.query(RoleBinding.workspace_id).filter(
            RoleBinding.user_id == user_id,
            RoleBinding.scope_type == ScopeType.WORKSPACE.value,
            RoleBinding.is_active == True,
            or_(
                RoleBinding.expires_at == None,
                RoleBinding.expires_at > now
            )
        ).all()
        
        return [b.workspace_id for b in bindings if b.workspace_id]
    
    @classmethod
    def get_accessible_documents(
        cls,
        db: Session,
        user_id: str,
        workspace_id: str,
        include_private: bool = False
    ) -> List[str]:
        """Get list of document IDs user can access in a workspace."""
        # Check workspace role
        if not cls.check_permission(db, user_id, "read", "workspace", workspace_id):
            return []
        
        # Query accessible documents
        query = db.query(Document.id).filter(
            Document.workspace_id == workspace_id,
            Document.deleted_at == None
        )
        
        if not include_private:
            query = query.filter(
                or_(
                    Document.owner_id == user_id,
                    Document.visibility != "private"
                )
            )
        
        return [d.id for d in query.all()]
    
    @classmethod
    def grant_role(
        cls,
        db: Session,
        user_id: str,
        role: str,
        scope_type: ScopeType,
        scope_id: str,
        granted_by_id: str,
        expires_at: Optional[datetime] = None
    ) -> RoleBinding:
        """Grant a role to a user at a specific scope."""
        # Create role binding
        binding = RoleBinding(
            user_id=user_id,
            role=role,
            scope_type=scope_type.value,
            granted_by_id=granted_by_id,
            expires_at=expires_at,
        )
        
        # Set the appropriate scope ID
        if scope_type == ScopeType.ORGANIZATION:
            binding.org_id = scope_id
        elif scope_type == ScopeType.WORKSPACE:
            binding.workspace_id = scope_id
        elif scope_type == ScopeType.PROJECT:
            binding.project_id = scope_id
        elif scope_type == ScopeType.DOCUMENT:
            binding.document_id = scope_id
        
        db.add(binding)
        db.commit()
        db.refresh(binding)
        
        return binding
    
    @classmethod
    def revoke_role(
        cls,
        db: Session,
        user_id: str,
        scope_type: ScopeType,
        scope_id: str
    ) -> bool:
        """Revoke a user's role at a specific scope."""
        query = db.query(RoleBinding).filter(
            RoleBinding.user_id == user_id,
            RoleBinding.scope_type == scope_type.value,
            RoleBinding.is_active == True
        )
        
        if scope_type == ScopeType.ORGANIZATION:
            query = query.filter(RoleBinding.org_id == scope_id)
        elif scope_type == ScopeType.WORKSPACE:
            query = query.filter(RoleBinding.workspace_id == scope_id)
        elif scope_type == ScopeType.PROJECT:
            query = query.filter(RoleBinding.project_id == scope_id)
        elif scope_type == ScopeType.DOCUMENT:
            query = query.filter(RoleBinding.document_id == scope_id)
        
        binding = query.first()
        
        if binding:
            binding.is_active = False
            db.commit()
            return True
        
        return False
