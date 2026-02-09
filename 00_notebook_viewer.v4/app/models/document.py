# -*- coding: utf-8 -*-
"""
Document Model
- Core content entity
- Version control
- Draft/Published states
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, JSON, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.workspace import Workspace
    from app.models.user import User
    from app.models.content import Comment, Highlight


class DocumentStatus(str, Enum):
    """Document publication status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class DocumentVisibility(str, Enum):
    """Document visibility level."""
    PRIVATE = "private"          # Only owner
    WORKSPACE = "workspace"      # Workspace members
    ORGANIZATION = "organization"  # All org members
    PUBLIC = "public"            # Anyone with link


class Document(Base):
    """Document model - core content entity."""
    
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Hierarchy
    workspace_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True
    )
    
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    parent_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Content
    title: Mapped[str] = mapped_column(String(500), index=True)
    slug: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(Text, default="")
    content_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📄")
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Frontmatter / Custom fields
    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Status & Visibility
    status: Mapped[str] = mapped_column(
        String(20), 
        default=DocumentStatus.DRAFT.value,
        index=True
    )
    visibility: Mapped[str] = mapped_column(
        String(20), 
        default=DocumentVisibility.WORKSPACE.value
    )
    
    # Ownership
    owner_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="RESTRICT"),
        index=True
    )
    
    last_editor_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Versioning
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    
    # Ordering
    position: Mapped[int] = mapped_column(Integer, default=0)
    
    # Stats
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Soft delete
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="documents"
    )
    
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id]
    )
    
    last_editor: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[last_editor_id]
    )
    
    parent: Mapped[Optional["Document"]] = relationship(
        "Document",
        remote_side=[id],
        backref="children"
    )
    
    versions: Mapped[List["DocumentVersion"]] = relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    
    highlights: Mapped[List["Highlight"]] = relationship(
        "Highlight",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_doc_workspace_status", "workspace_id", "status"),
        Index("idx_doc_owner_status", "owner_id", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<Document {self.title[:30]}>"
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class DocumentVersion(Base):
    """Document version history - Git-like versioning."""
    
    __tablename__ = "document_versions"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    document_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True
    )
    
    # Version info
    version_number: Mapped[int] = mapped_column(Integer)
    
    # Content snapshot
    title: Mapped[str] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text)
    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Author
    author_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Change info
    change_summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Stats
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    char_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="versions"
    )
    
    author: Mapped[Optional["User"]] = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index("idx_docver_doc_version", "document_id", "version_number"),
    )
    
    def __repr__(self) -> str:
        return f"<DocumentVersion {self.document_id}:v{self.version_number}>"
