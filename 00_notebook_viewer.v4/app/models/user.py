# -*- coding: utf-8 -*-
"""
User Model
- Core user entity for authentication
- Profile information
- Multi-tenant association
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.workspace import Workspace
    from app.models.permission import RoleBinding


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    # Profile
    display_name: Mapped[str] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Settings & Preferences
    theme: Mapped[str] = mapped_column(String(20), default="light")
    locale: Mapped[str] = mapped_column(String(10), default="ko")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Seoul")
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Organization (optional - for personal accounts)
    default_org_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Relationships
    owned_organizations: Mapped[List["Organization"]] = relationship(
        "Organization",
        back_populates="owner",
        foreign_keys="Organization.owner_id"
    )
    
    role_bindings: Mapped[List["RoleBinding"]] = relationship(
        "RoleBinding",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="RoleBinding.user_id"
    )
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    @property
    def full_name(self) -> str:
        return self.display_name or self.username


class RefreshToken(Base):
    """Refresh token for JWT authentication."""
    
    __tablename__ = "refresh_tokens"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    # Device/session info
    device_info: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    
    # Validity
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User")
