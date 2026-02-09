# -*- coding: utf-8 -*-
"""
Workspace Model
- Team/Project group level
- Contains documents and projects
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.document import Document


class Workspace(Base):
    """Workspace model - team/project group level."""
    
    __tablename__ = "workspaces"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Parent organization
    org_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True
    )
    
    # Basic info
    name: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📁")
    
    # Settings
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    default_visibility: Mapped[str] = mapped_column(
        String(20), 
        default="workspace"
    )  # private, workspace, organization
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Ordering
    position: Mapped[int] = mapped_column(default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="workspaces"
    )
    
    documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="workspace",
        cascade="all, delete-orphan"
    )
    
    # Unique constraint: slug unique within organization
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )
    
    def __repr__(self) -> str:
        return f"<Workspace {self.name}>"


class Project(Base):
    """Project within a workspace - optional grouping layer."""
    
    __tablename__ = "projects"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    workspace_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True
    )
    
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📂")
    color: Mapped[str] = mapped_column(String(7), default="#1f7aec")
    
    # Ordering
    position: Mapped[int] = mapped_column(default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace")
    
    def __repr__(self) -> str:
        return f"<Project {self.name}>"
