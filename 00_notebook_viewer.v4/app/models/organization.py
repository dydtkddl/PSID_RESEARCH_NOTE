# -*- coding: utf-8 -*-
"""
Organization Model
- Top-level multi-tenant entity
- Company/Institute level
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace


class Organization(Base):
    """Organization model - top level of multi-tenant hierarchy."""
    
    __tablename__ = "organizations"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Basic info
    name: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Branding
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(7), default="#1f7aec")
    
    # Settings
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    default_theme: Mapped[str] = mapped_column(String(20), default="light")
    
    # Ownership
    owner_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    plan: Mapped[str] = mapped_column(String(50), default="free")  # free, pro, enterprise
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    owner: Mapped["User"] = relationship(
        "User", 
        back_populates="owned_organizations",
        foreign_keys=[owner_id]
    )
    
    workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace",
        back_populates="organization",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Organization {self.name}>"
