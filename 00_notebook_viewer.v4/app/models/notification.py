# -*- coding: utf-8 -*-
"""
Invite and Notification Models
- Workspace invitations with invite codes
- User notifications / inbox
"""

import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InviteStatus(str, Enum):
    """Invite status."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"


class NotificationType(str, Enum):
    """Notification types."""
    INVITE = "invite"
    MENTION = "mention"
    COMMENT = "comment"
    SHARE = "share"
    SYSTEM = "system"


class Invite(Base):
    """Workspace invitation with invite code."""
    
    __tablename__ = "invites"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Invite code (8 chars)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    
    # Target workspace
    workspace_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True
    )
    
    # Who created the invite
    created_by_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE")
    )
    
    # Who accepted (if any)
    accepted_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Role to grant
    role: Mapped[str] = mapped_column(String(20), default="viewer")
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default=InviteStatus.PENDING.value)
    
    # Usage limits
    max_uses: Mapped[int] = mapped_column(Integer, default=1)
    use_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    @staticmethod
    def generate_code():
        """Generate a unique invite code."""
        return secrets.token_urlsafe(6)[:8].upper()
    
    @property
    def is_valid(self) -> bool:
        """Check if invite is still valid."""
        if self.status != InviteStatus.PENDING.value:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        if self.max_uses > 0 and self.use_count >= self.max_uses:
            return False
        return True


class Notification(Base):
    """User notification / inbox item."""
    
    __tablename__ = "notifications"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Target user
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    # Type
    type: Mapped[str] = mapped_column(String(20), default=NotificationType.SYSTEM.value)
    
    # Content
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    
    # Optional link
    link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Related entities
    workspace_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    document_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    from_user_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    # Status
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
