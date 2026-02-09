# -*- coding: utf-8 -*-
"""
Document Service
- CRUD operations
- Version management  
- Markdown rendering
"""

import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path

import markdown
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func

from app.config import settings
from app.models.document import Document, DocumentVersion, DocumentStatus, DocumentVisibility
from app.models.workspace import Workspace
from app.models.content import Comment, Highlight, Tag, DocumentTag, Favorite, RecentView
from app.services.security import SecurityService


class DocumentService:
    """Document management service."""
    
    # Markdown processor
    MD_EXTENSIONS = settings.MD_EXTENSIONS
    MD_EXTENSION_CONFIGS = {
        "pymdownx.arithmatex": {
            "generic": True,
            "smart_dollar": False,  # LaTeX $ 문자를 항상 수식으로 인식
        },
        "pymdownx.highlight": {
            "auto_title": True,
            "linenums": True,
        },
        "pymdownx.tasklist": {
            "clickable_checkbox": True,
        },
    }
    
    @classmethod
    def render_markdown(cls, content: str) -> str:
        """Render Markdown to HTML."""
        if not content:
            return ""
        
        try:
            md = markdown.Markdown(
                extensions=cls.MD_EXTENSIONS,
                extension_configs=cls.MD_EXTENSION_CONFIGS
            )
            html = md.convert(content)
            return SecurityService.sanitize_html(html)
        except Exception as e:
            return f"<p>Error rendering markdown: {str(e)}</p>"
    
    @classmethod
    def extract_frontmatter(cls, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter from markdown content."""
        import yaml
        
        # Normalize line endings
        content = content.replace('\r\n', '\n')
        
        if not content.startswith("---\n"):
            return {}, content
        
        try:
            # Split on "---\n" to properly parse YAML frontmatter
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                # parts[0] is empty, parts[1] is YAML, parts[2] is body
                raw_yaml = parts[1]
                body = parts[2].strip()
                
                frontmatter = yaml.safe_load(raw_yaml)
                return frontmatter or {}, body
            
            return {}, content
        except Exception as e:
            print(f"Frontmatter parse error: {e}")
            return {}, content
    
    @classmethod
    def compute_content_hash(cls, content: str) -> str:
        """Compute hash of content for comparison."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    @classmethod
    def count_words(cls, content: str) -> int:
        """Count words in content."""
        import re
        # Remove markdown syntax
        text = re.sub(r'[#*`\[\]()!]', '', content)
        words = text.split()
        return len(words)
    
    @classmethod
    def create_document(
        cls,
        db: Session,
        workspace_id: str,
        title: str,
        content: str,
        owner_id: str,
        project_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        visibility: DocumentVisibility = DocumentVisibility.WORKSPACE,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """Create a new document."""
        # Generate slug
        slug = SecurityService.generate_slug(title)
        
        # Parse frontmatter
        frontmatter, body = cls.extract_frontmatter(content)
        if metadata:
            frontmatter.update(metadata)
        
        # Render HTML
        content_html = cls.render_markdown(body)
        
        document = Document(
            workspace_id=workspace_id,
            project_id=project_id,
            parent_id=parent_id,
            title=title,
            slug=slug,
            content=content,
            content_html=content_html,
            doc_metadata=frontmatter,
            owner_id=owner_id,
            visibility=visibility.value,
            status=DocumentStatus.DRAFT.value,
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Create initial version
        cls._create_version(db, document, owner_id, "Initial version")
        
        return document
    
    @classmethod
    def update_document(
        cls,
        db: Session,
        document: Document,
        editor_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        change_summary: Optional[str] = None
    ) -> Document:
        """Update an existing document."""
        content_changed = False
        
        if title and title != document.title:
            document.title = title
            document.slug = SecurityService.generate_slug(title)
        
        if content is not None and content != document.content:
            document.content = content
            frontmatter, body = cls.extract_frontmatter(content)
            document.content_html = cls.render_markdown(body)
            
            # Merge frontmatter with existing metadata
            existing_meta = document.doc_metadata if isinstance(document.doc_metadata, dict) else {}
            merged_meta = existing_meta.copy() if existing_meta else {}
            merged_meta.update(frontmatter)
            document.doc_metadata = merged_meta
            
            content_changed = True
        elif content is not None and not document.doc_metadata:
            # Force parse frontmatter if doc_metadata is empty (migration case)
            frontmatter, body = cls.extract_frontmatter(content)
            if frontmatter:
                document.doc_metadata = frontmatter
                document.content_html = cls.render_markdown(body)
        
        if metadata:
            existing_meta = document.doc_metadata if isinstance(document.doc_metadata, dict) else {}
            merged = existing_meta.copy() if existing_meta else {}
            merged.update(metadata)
            document.doc_metadata = merged
        
        document.last_editor_id = editor_id
        document.updated_at = datetime.utcnow()
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Create new version if content changed
        if content_changed:
            document.current_version += 1
            db.add(document)
            db.commit()
            cls._create_version(db, document, editor_id, change_summary)
        
        return document
    
    @classmethod
    def _create_version(
        cls,
        db: Session,
        document: Document,
        author_id: str,
        change_summary: Optional[str] = None
    ) -> DocumentVersion:
        """Create a new version snapshot."""
        version = DocumentVersion(
            document_id=document.id,
            version_number=document.current_version,
            title=document.title,
            content=document.content,
            metadata=document.doc_metadata or {},
            author_id=author_id,
            change_summary=change_summary,
            word_count=cls.count_words(document.content),
            char_count=len(document.content),
        )
        
        db.add(version)
        db.commit()
        db.refresh(version)
        
        return version
    
    @classmethod
    def get_document(
        cls,
        db: Session,
        document_id: str,
        include_deleted: bool = False
    ) -> Optional[Document]:
        """Get document by ID."""
        query = db.query(Document).filter(Document.id == document_id)
        
        if not include_deleted:
            query = query.filter(Document.deleted_at == None)
        
        return query.first()
    
    @classmethod
    def get_document_by_slug(
        cls,
        db: Session,
        workspace_id: str,
        slug: str
    ) -> Optional[Document]:
        """Get document by workspace and slug."""
        return db.query(Document).filter(
            Document.workspace_id == workspace_id,
            Document.slug == slug,
            Document.deleted_at == None
        ).first()
    
    @classmethod
    def list_documents(
        cls,
        db: Session,
        workspace_id: str,
        project_id: Optional[str] = None,
        status: Optional[DocumentStatus] = None,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owner_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "updated_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Document], int]:
        """List documents with filtering and pagination."""
        query = db.query(Document).filter(
            Document.workspace_id == workspace_id,
            Document.deleted_at == None
        )
        
        if project_id:
            query = query.filter(Document.project_id == project_id)
        
        if status:
            query = query.filter(Document.status == status.value)
        
        if owner_id:
            query = query.filter(Document.owner_id == owner_id)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Document.title.ilike(search_term),
                    Document.content.ilike(search_term)
                )
            )
        
        # TODO: Tag filtering
        
        # Count total
        total = query.count()
        
        # Sorting
        sort_column = getattr(Document, sort_by, Document.updated_at)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Pagination
        offset = (page - 1) * page_size
        documents = query.offset(offset).limit(page_size).all()
        
        return documents, total
    
    @classmethod
    def delete_document(
        cls,
        db: Session,
        document: Document,
        permanent: bool = False
    ) -> bool:
        """Delete a document (soft delete by default)."""
        if permanent:
            db.delete(document)
        else:
            document.deleted_at = datetime.utcnow()
            document.status = DocumentStatus.DELETED.value
            db.add(document)
        
        db.commit()
        return True
    
    @classmethod
    def restore_document(cls, db: Session, document: Document) -> Document:
        """Restore a soft-deleted document."""
        document.deleted_at = None
        document.status = DocumentStatus.DRAFT.value
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    
    @classmethod
    def publish_document(cls, db: Session, document: Document) -> Document:
        """Publish a draft document."""
        document.status = DocumentStatus.PUBLISHED.value
        document.published_at = datetime.utcnow()
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    
    @classmethod
    def get_versions(
        cls,
        db: Session,
        document_id: str,
        limit: int = 50
    ) -> List[DocumentVersion]:
        """Get version history for a document."""
        return db.query(DocumentVersion).filter(
            DocumentVersion.document_id == document_id
        ).order_by(
            DocumentVersion.version_number.desc()
        ).limit(limit).all()
    
    @classmethod
    def get_version(
        cls,
        db: Session,
        document_id: str,
        version_number: int
    ) -> Optional[DocumentVersion]:
        """Get a specific version."""
        return db.query(DocumentVersion).filter(
            DocumentVersion.document_id == document_id,
            DocumentVersion.version_number == version_number
        ).first()
    
    @classmethod
    def compare_versions(
        cls,
        db: Session,
        document_id: str,
        version_a: int,
        version_b: int
    ) -> Dict[str, Any]:
        """Compare two versions of a document."""
        v_a = cls.get_version(db, document_id, version_a)
        v_b = cls.get_version(db, document_id, version_b)
        
        if not v_a or not v_b:
            return {"error": "Version not found"}
        
        # Simple diff info (could use difflib for detailed diff)
        return {
            "version_a": {
                "number": v_a.version_number,
                "title": v_a.title,
                "word_count": v_a.word_count,
                "author_id": v_a.author_id,
                "created_at": v_a.created_at.isoformat(),
            },
            "version_b": {
                "number": v_b.version_number,
                "title": v_b.title,
                "word_count": v_b.word_count,
                "author_id": v_b.author_id,
                "created_at": v_b.created_at.isoformat(),
            },
            "title_changed": v_a.title != v_b.title,
            "word_count_diff": v_b.word_count - v_a.word_count,
        }
    
    @classmethod
    def record_view(cls, db: Session, document_id: str, user_id: str) -> None:
        """Record a document view."""
        # Update document view count
        db.query(Document).filter(
            Document.id == document_id
        ).update({
            Document.view_count: Document.view_count + 1
        })
        
        # Add/update recent view
        recent = db.query(RecentView).filter(
            RecentView.user_id == user_id,
            RecentView.document_id == document_id
        ).first()
        
        if recent:
            recent.viewed_at = datetime.utcnow()
        else:
            recent = RecentView(
                user_id=user_id,
                document_id=document_id
            )
            db.add(recent)
        
        db.commit()
    
    @classmethod
    def get_recent_documents(
        cls,
        db: Session,
        user_id: str,
        limit: int = 10
    ) -> List[Document]:
        """Get user's recently viewed documents."""
        recent_views = db.query(RecentView).filter(
            RecentView.user_id == user_id
        ).order_by(
            RecentView.viewed_at.desc()
        ).limit(limit).all()
        
        doc_ids = [rv.document_id for rv in recent_views]
        
        if not doc_ids:
            return []
        
        documents = db.query(Document).filter(
            Document.id.in_(doc_ids),
            Document.deleted_at == None
        ).all()
        
        # Maintain order
        doc_map = {d.id: d for d in documents}
        return [doc_map[did] for did in doc_ids if did in doc_map]
    
    @classmethod
    def toggle_favorite(
        cls,
        db: Session,
        user_id: str,
        document_id: str
    ) -> bool:
        """Toggle favorite status. Returns True if now favorited."""
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.document_id == document_id
        ).first()
        
        if favorite:
            db.delete(favorite)
            db.commit()
            return False
        else:
            favorite = Favorite(user_id=user_id, document_id=document_id)
            db.add(favorite)
            db.commit()
            return True
    
    @classmethod
    def get_favorites(
        cls,
        db: Session,
        user_id: str,
        limit: int = 50
    ) -> List[Document]:
        """Get user's favorite documents."""
        favorites = db.query(Favorite).filter(
            Favorite.user_id == user_id
        ).order_by(
            Favorite.created_at.desc()
        ).limit(limit).all()
        
        doc_ids = [f.document_id for f in favorites]
        
        if not doc_ids:
            return []
        
        return db.query(Document).filter(
            Document.id.in_(doc_ids),
            Document.deleted_at == None
        ).all()
    
    @classmethod
    def is_favorited(cls, db: Session, user_id: str, document_id: str) -> bool:
        """Check if document is favorited by user."""
        return db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.document_id == document_id
        ).first() is not None
