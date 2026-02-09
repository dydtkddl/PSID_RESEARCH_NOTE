# -*- coding: utf-8 -*-
"""
Audit Log Model
- Track all important actions
- Security compliance
- Change history
"""

import uuid
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import String, DateTime, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AuditAction(str, Enum):
    """Types of auditable actions."""
    # Auth
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGED = "password_changed"
    
    # User management
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    
    # Organization
    ORG_CREATED = "org_created"
    ORG_UPDATED = "org_updated"
    ORG_DELETED = "org_deleted"
    
    # Workspace
    WORKSPACE_CREATED = "workspace_created"
    WORKSPACE_UPDATED = "workspace_updated"
    WORKSPACE_DELETED = "workspace_deleted"
    
    # Document
    DOC_CREATED = "doc_created"
    DOC_UPDATED = "doc_updated"
    DOC_DELETED = "doc_deleted"
    DOC_VIEWED = "doc_viewed"
    DOC_EXPORTED = "doc_exported"
    DOC_PUBLISHED = "doc_published"
    DOC_RESTORED = "doc_restored"
    
    # Permission
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_REVOKED = "permission_revoked"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REMOVED = "role_removed"
    
    # Content
    COMMENT_ADDED = "comment_added"
    COMMENT_DELETED = "comment_deleted"
    HIGHLIGHT_ADDED = "highlight_added"
    HIGHLIGHT_DELETED = "highlight_deleted"


class AuditLog(Base):
    """Audit log for tracking all important actions."""
    
    __tablename__ = "audit_logs"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # When
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        index=True
    )
    
    # Who
    user_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    user_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Context
    org_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    workspace_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # What
    action: Mapped[str] = mapped_column(String(50), index=True)
    
    # On what resource
    resource_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    resource_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Details
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    old_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Request info
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    # Status
    success: Mapped[bool] = mapped_column(default=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    # Indexes
    __table_args__ = (
        Index("idx_audit_user_action", "user_id", "action"),
        Index("idx_audit_org_action", "org_id", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_timestamp", "timestamp"),
    )
    
    def __repr__(self) -> str:
        return f"<AuditLog {self.action} by {self.user_email} at {self.timestamp}>"
