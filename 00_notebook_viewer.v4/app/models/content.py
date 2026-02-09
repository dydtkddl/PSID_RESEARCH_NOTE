# -*- coding: utf-8 -*-
"""
Content Models
- Comments (threaded)
- Highlights
- Tags
- Favorites
- Recent views
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document


class Comment(Base):
    """Threaded comments on documents."""
    
    __tablename__ = "comments"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Parent document
    document_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True
    )
    
    # Threading
    parent_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Author
    author_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    # Content
    content: Mapped[str] = mapped_column(Text)
    content_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Position in document (optional - for inline comments)
    anchor_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    anchor_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    anchor_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Soft delete
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="comments"
    )
    
    author: Mapped["User"] = relationship(
        "User",
        foreign_keys=[author_id]
    )
    
    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side=[id],
        backref="replies"
    )
    
    resolved_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[resolved_by_id]
    )
    
    __table_args__ = (
        Index("idx_comment_doc_parent", "document_id", "parent_id"),
    )
    
    def __repr__(self) -> str:
        return f"<Comment {self.id[:8]} on {self.document_id[:8]}>"


class Highlight(Base):
    """Text highlights on documents."""
    
    __tablename__ = "highlights"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Parent document
    document_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True
    )
    
    # Author
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    # Position
    start_offset: Mapped[int] = mapped_column(Integer)
    end_offset: Mapped[int] = mapped_column(Integer)
    
    # Content
    text: Mapped[str] = mapped_column(Text)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Styling
    color: Mapped[str] = mapped_column(String(7), default="#fff59d")
    
    # Version tracking
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="highlights"
    )
    
    user: Mapped["User"] = relationship("User")
    
    __table_args__ = (
        Index("idx_highlight_doc_user", "document_id", "user_id"),
    )
    
    def __repr__(self) -> str:
        return f"<Highlight {self.id[:8]} on {self.document_id[:8]}>"


class Tag(Base):
    """Tags for documents."""
    
    __tablename__ = "tags"
    
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    # Scope
    workspace_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True
    )
    
    # Tag info
    name: Mapped[str] = mapped_column(String(100), index=True)
    slug: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(7), default="#1f7aec")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_tag_workspace_name", "workspace_id", "name"),
    )
    
    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class DocumentTag(Base):
    """Many-to-many relationship between documents and tags."""
    
    __tablename__ = "document_tags"
    
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
    
    tag_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("tags.id", ondelete="CASCADE"),
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_doctag_doc", "document_id"),
        Index("idx_doctag_tag", "tag_id"),
    )


class Favorite(Base):
    """User favorites/bookmarks."""
    
    __tablename__ = "favorites"
    
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
    
    document_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User")
    document: Mapped["Document"] = relationship("Document")
    
    __table_args__ = (
        Index("idx_favorite_user_doc", "user_id", "document_id", unique=True),
    )


class RecentView(Base):
    """Recently viewed documents per user."""
    
    __tablename__ = "recent_views"
    
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
    
    document_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True
    )
    
    viewed_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        index=True
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User")
    document: Mapped["Document"] = relationship("Document")
    
    __table_args__ = (
        Index("idx_recent_user_time", "user_id", "viewed_at"),
    )
