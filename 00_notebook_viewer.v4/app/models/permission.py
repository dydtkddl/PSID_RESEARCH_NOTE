# -*- coding: utf-8 -*-
"""
Permission & RBAC Models
- Role definitions
- Role bindings (user-role-scope)
- Granular permissions
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class RoleType(str, Enum):
    """Predefined role types with default permissions."""
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"


# Default permissions for each role
ROLE_PERMISSIONS = {
    RoleType.OWNER: {
        "read": True,
        "write": True,
        "delete": True,
        "manage_members": True,
        "manage_settings": True,
        "manage_permissions": True,
        "export": True,
        "admin": True,
    },
    RoleType.ADMIN: {
        "read": True,
        "write": True,
        "delete": True,
        "manage_members": True,
        "manage_settings": True,
        "manage_permissions": False,
        "export": True,
        "admin": False,
    },
    RoleType.EDITOR: {
        "read": True,
        "write": True,
        "delete": False,
        "manage_members": False,
        "manage_settings": False,
        "manage_permissions": False,
        "export": True,
        "admin": False,
    },
    RoleType.VIEWER: {
        "read": True,
        "write": False,
        "delete": False,
        "manage_members": False,
        "manage_settings": False,
        "manage_permissions": False,
        "export": True,
        "admin": False,
    },
    RoleType.GUEST: {
        "read": True,
        "write": False,
        "delete": False,
        "manage_members": False,
        "manage_settings": False,
        "manage_permissions": False,
        "export": False,
        "admin": False,
    },
}


class ScopeType(str, Enum):
    """Scope level for role binding."""
    ORGANIZATION = "organization"
    WORKSPACE = "workspace"
    PROJECT = "project"
    DOCUMENT = "document"


class Role(Base):
    """Custom role definition (for org-specific roles)."""
    
    __tablename__ = "roles"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Scope
    org_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )  # NULL = system-wide role
    
    # Role info
    name: Mapped[str] = mapped_column(String(100))
    display_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Permissions mapping
    permissions: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Is this a predefined system role?
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<Role {self.name}>"


class RoleBinding(Base):
    """
    User-Role-Scope binding.
    
    Determines what role a user has at what scope.
    Precedence: Document > Project > Workspace > Organization
    """
    
    __tablename__ = "role_bindings"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Who
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    # What role
    role: Mapped[str] = mapped_column(String(50), index=True)  # RoleType value or custom role name
    
    # Where (scope) - Only one of these should be set based on scope_type
    scope_type: Mapped[str] = mapped_column(String(20), index=True)
    
    org_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    document_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Who granted this
    granted_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="role_bindings",
        foreign_keys=[user_id]
    )
    
    granted_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[granted_by_id]
    )
    
    # Indexes and constraints
    __table_args__ = (
        Index("idx_rb_user_scope", "user_id", "scope_type"),
        Index("idx_rb_org", "org_id", "user_id"),
        Index("idx_rb_workspace", "workspace_id", "user_id"),
    )
    
    def __repr__(self) -> str:
        return f"<RoleBinding user={self.user_id} role={self.role} scope={self.scope_type}>"
    
    @property
    def scope_id(self) -> Optional[str]:
        """Get the ID of the scoped resource."""
        if self.scope_type == ScopeType.ORGANIZATION:
            return self.org_id
        elif self.scope_type == ScopeType.WORKSPACE:
            return self.workspace_id
        elif self.scope_type == ScopeType.PROJECT:
            return self.project_id
        elif self.scope_type == ScopeType.DOCUMENT:
            return self.document_id
        return None


class Permission(Base):
    """
    Fine-grained permission override.
    
    For cases where RBAC roles are too coarse-grained.
    Example: Viewer role but with comment permission.
    """
    
    __tablename__ = "permissions"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Who
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    # What resource
    resource_type: Mapped[str] = mapped_column(String(50))  # document, workspace, etc.
    resource_id: Mapped[str] = mapped_column(String(36), index=True)
    
    # What permission
    permission: Mapped[str] = mapped_column(String(50))  # read, write, comment, etc.
    
    # Allow or deny
    allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    granted_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    __table_args__ = (
        UniqueConstraint("user_id", "resource_type", "resource_id", "permission"),
        Index("idx_perm_resource", "resource_type", "resource_id"),
    )
    
    def __repr__(self) -> str:
        action = "allow" if self.allowed else "deny"
        return f"<Permission {action} {self.permission} on {self.resource_type}:{self.resource_id}>"
