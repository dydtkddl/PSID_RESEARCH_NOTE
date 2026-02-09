# -*- coding: utf-8 -*-
"""
Documents API Router
- CRUD operations
- Version management
- Comments & Highlights
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentStatus, DocumentVisibility
from app.models.content import Comment, Highlight
from app.services.document import DocumentService
from app.services.permission import PermissionService
from app.services.audit import AuditService
from app.models.audit import AuditAction
from app.api.schemas import (
    DocumentCreate, DocumentUpdate, DocumentResponse, DocumentList, DocumentListItem,
    DocumentVersionResponse, CommentCreate, CommentUpdate, CommentResponse,
    HighlightCreate, HighlightUpdate, HighlightResponse, MessageResponse
)
from app.api.deps import get_current_active_user, get_db


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    data: DocumentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new document."""
    workspace_id = data.workspace_id
    if not workspace_id:
        raise HTTPException(status_code=400, detail="workspace_id is required")
    
    # Check workspace write permission
    if not PermissionService.check_permission(db, current_user.id, "write", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    visibility = DocumentVisibility(data.visibility) if data.visibility else DocumentVisibility.WORKSPACE
    
    document = DocumentService.create_document(
        db=db,
        workspace_id=workspace_id,
        title=data.title,
        content=data.content,
        owner_id=current_user.id,
        project_id=data.project_id,
        parent_id=data.parent_id,
        visibility=visibility,
        metadata=data.metadata
    )
    
    # Audit
    AuditService.log_document_action(
        db,
        action=AuditAction.DOC_CREATED,
        document_id=document.id,
        document_title=document.title,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=workspace_id,
    )
    
    return _document_to_response(document, db, current_user.id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a document by ID."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permission
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Record view
    DocumentService.record_view(db, document_id, current_user.id)
    
    return _document_to_response(document, db, current_user.id)


@router.get("", response_model=DocumentList)
def list_documents(
    workspace_id: str,
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    owner_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = "updated_at",
    sort_order: str = "desc",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List documents in a workspace."""
    # Check workspace read permission
    if not PermissionService.check_permission(db, current_user.id, "read", "workspace", workspace_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    doc_status = DocumentStatus(status) if status else None
    
    documents, total = DocumentService.list_documents(
        db=db,
        workspace_id=workspace_id,
        project_id=project_id,
        status=doc_status,
        search=search,
        owner_id=owner_id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    items = [
        DocumentListItem(
            id=doc.id,
            title=doc.title,
            slug=doc.slug,
            icon=doc.icon,
            status=doc.status,
            owner_id=doc.owner_id,
            updated_at=doc.updated_at
        )
        for doc in documents
    ]
    
    return DocumentList(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    data: DocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permission
    if not PermissionService.can_write(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Store old values for audit
    old_values = {
        "title": document.title,
        "content_hash": DocumentService.compute_content_hash(document.content)
    }
    
    document = DocumentService.update_document(
        db=db,
        document=document,
        editor_id=current_user.id,
        title=data.title,
        content=data.content,
        metadata=data.metadata,
        change_summary=data.change_summary
    )
    
    # Audit
    AuditService.log_document_action(
        db,
        action=AuditAction.DOC_UPDATED,
        document_id=document.id,
        document_title=document.title,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=document.workspace_id,
        old_values=old_values,
        new_values={
            "title": document.title,
            "content_hash": DocumentService.compute_content_hash(document.content)
        }
    )
    
    return _document_to_response(document, db, current_user.id)


@router.delete("/{document_id}", response_model=MessageResponse)
def delete_document(
    document_id: str,
    permanent: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document (soft delete by default)."""
    document = DocumentService.get_document(db, document_id, include_deleted=True)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permission
    if not PermissionService.can_delete(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    DocumentService.delete_document(db, document, permanent=permanent)
    
    # Audit
    AuditService.log_document_action(
        db,
        action=AuditAction.DOC_DELETED,
        document_id=document.id,
        document_title=document.title,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=document.workspace_id,
    )
    
    action = "permanently deleted" if permanent else "moved to trash"
    return MessageResponse(message=f"Document {action}")


@router.post("/{document_id}/restore", response_model=DocumentResponse)
def restore_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Restore a deleted document."""
    document = DocumentService.get_document(db, document_id, include_deleted=True)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.is_deleted:
        raise HTTPException(status_code=400, detail="Document is not deleted")
    
    # Check permission
    if not PermissionService.can_write(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    document = DocumentService.restore_document(db, document)
    
    # Audit
    AuditService.log_document_action(
        db,
        action=AuditAction.DOC_RESTORED,
        document_id=document.id,
        document_title=document.title,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=document.workspace_id,
    )
    
    return _document_to_response(document, db, current_user.id)


@router.post("/{document_id}/publish", response_model=DocumentResponse)
def publish_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Publish a draft document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permission
    if not PermissionService.can_write(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    document = DocumentService.publish_document(db, document)
    
    # Audit
    AuditService.log_document_action(
        db,
        action=AuditAction.DOC_PUBLISHED,
        document_id=document.id,
        document_title=document.title,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=document.workspace_id,
    )
    
    return _document_to_response(document, db, current_user.id)


# ============ Versions ============

@router.get("/{document_id}/versions", response_model=List[DocumentVersionResponse])
def list_versions(
    document_id: str,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get version history for a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    versions = DocumentService.get_versions(db, document_id, limit=limit)
    
    return [
        DocumentVersionResponse(
            id=v.id,
            document_id=v.document_id,
            version_number=v.version_number,
            title=v.title,
            content=v.content,
            author_id=v.author_id,
            change_summary=v.change_summary,
            word_count=v.word_count,
            created_at=v.created_at
        )
        for v in versions
    ]


@router.get("/{document_id}/versions/{version_number}", response_model=DocumentVersionResponse)
def get_version(
    document_id: str,
    version_number: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific version of a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    version = DocumentService.get_version(db, document_id, version_number)
    
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    return DocumentVersionResponse(
        id=version.id,
        document_id=version.document_id,
        version_number=version.version_number,
        title=version.title,
        content=version.content,
        author_id=version.author_id,
        change_summary=version.change_summary,
        word_count=version.word_count,
        created_at=version.created_at
    )


# ============ Favorites ============

@router.post("/{document_id}/favorite", response_model=MessageResponse)
def toggle_favorite(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Toggle favorite status for a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    is_favorite = DocumentService.toggle_favorite(db, current_user.id, document_id)
    
    action = "added to" if is_favorite else "removed from"
    return MessageResponse(message=f"Document {action} favorites")


# ============ Comments ============

@router.get("/{document_id}/comments", response_model=List[CommentResponse])
def list_comments(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List comments on a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Get top-level comments
    comments = db.query(Comment).filter(
        Comment.document_id == document_id,
        Comment.parent_id == None,
        Comment.deleted_at == None
    ).order_by(Comment.created_at.asc()).all()
    
    def build_response(comment: Comment) -> CommentResponse:
        author = db.query(User).filter(User.id == comment.author_id).first()
        replies = db.query(Comment).filter(
            Comment.parent_id == comment.id,
            Comment.deleted_at == None
        ).order_by(Comment.created_at.asc()).all()
        
        return CommentResponse(
            id=comment.id,
            document_id=comment.document_id,
            parent_id=comment.parent_id,
            author_id=comment.author_id,
            author_name=author.display_name if author else None,
            content=comment.content,
            anchor_text=comment.anchor_text,
            is_resolved=comment.is_resolved,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            replies=[build_response(r) for r in replies]
        )
    
    return [build_response(c) for c in comments]


@router.post("/{document_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    document_id: str,
    data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a comment on a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    comment = Comment(
        document_id=document_id,
        parent_id=data.parent_id,
        author_id=current_user.id,
        content=data.content,
        anchor_start=data.anchor_start,
        anchor_end=data.anchor_end,
        anchor_text=data.anchor_text,
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # Audit
    AuditService.log(
        db,
        action=AuditAction.COMMENT_ADDED,
        user_id=current_user.id,
        user_email=current_user.email,
        workspace_id=document.workspace_id,
        resource_type="comment",
        resource_id=comment.id,
        details={"document_id": document_id}
    )
    
    return CommentResponse(
        id=comment.id,
        document_id=comment.document_id,
        parent_id=comment.parent_id,
        author_id=comment.author_id,
        author_name=current_user.display_name,
        content=comment.content,
        is_resolved=comment.is_resolved,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        replies=[]
    )


@router.delete("/{document_id}/comments/{comment_id}", response_model=MessageResponse)
def delete_comment(
    document_id: str,
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a comment."""
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.document_id == document_id
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Only author or admin can delete
    if comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    from datetime import datetime
    comment.deleted_at = datetime.utcnow()
    db.commit()
    
    return MessageResponse(message="Comment deleted")


# ============ Highlights ============

@router.get("/{document_id}/highlights", response_model=List[HighlightResponse])
def list_highlights(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List highlights on a document for current user."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    highlights = db.query(Highlight).filter(
        Highlight.document_id == document_id,
        Highlight.user_id == current_user.id
    ).order_by(Highlight.start_offset).all()
    
    return [
        HighlightResponse(
            id=h.id,
            document_id=h.document_id,
            user_id=h.user_id,
            start_offset=h.start_offset,
            end_offset=h.end_offset,
            text=h.text,
            note=h.note,
            color=h.color,
            created_at=h.created_at
        )
        for h in highlights
    ]


@router.post("/{document_id}/highlights", response_model=HighlightResponse, status_code=status.HTTP_201_CREATED)
def create_highlight(
    document_id: str,
    data: HighlightCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a highlight on a document."""
    document = DocumentService.get_document(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    highlight = Highlight(
        document_id=document_id,
        user_id=current_user.id,
        start_offset=data.start_offset,
        end_offset=data.end_offset,
        text=data.text,
        note=data.note,
        color=data.color,
        content_hash=data.content_hash,
    )
    
    db.add(highlight)
    db.commit()
    db.refresh(highlight)
    
    return HighlightResponse(
        id=highlight.id,
        document_id=highlight.document_id,
        user_id=highlight.user_id,
        start_offset=highlight.start_offset,
        end_offset=highlight.end_offset,
        text=highlight.text,
        note=highlight.note,
        color=highlight.color,
        created_at=highlight.created_at
    )


@router.delete("/{document_id}/highlights/{highlight_id}", response_model=MessageResponse)
def delete_highlight(
    document_id: str,
    highlight_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a highlight."""
    highlight = db.query(Highlight).filter(
        Highlight.id == highlight_id,
        Highlight.document_id == document_id,
        Highlight.user_id == current_user.id
    ).first()
    
    if not highlight:
        raise HTTPException(status_code=404, detail="Highlight not found")
    
    db.delete(highlight)
    db.commit()
    
    return MessageResponse(message="Highlight deleted")


# ============ File Upload ============

from fastapi import File, UploadFile
from pathlib import Path
import uuid as uuid_lib
import os

UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "static_new" / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    # Documents
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx",
    # Data
    ".csv", ".json", ".yaml", ".yml", ".xml",
    # Text
    ".txt", ".md", ".rst", ".log",
    # Archives
    ".zip", ".tar", ".gz",
}

FILE_TYPE_ICONS = {
    ".pdf": "ri-file-pdf-line",
    ".csv": "ri-file-excel-line",
    ".xlsx": "ri-file-excel-line",
    ".xls": "ri-file-excel-line",
    ".docx": "ri-file-word-line",
    ".doc": "ri-file-word-line",
    ".pptx": "ri-file-ppt-line",
    ".json": "ri-code-s-slash-line",
    ".yaml": "ri-code-s-slash-line",
    ".yml": "ri-code-s-slash-line",
    ".zip": "ri-file-zip-line",
    ".tar": "ri-file-zip-line",
    ".gz": "ri-file-zip-line",
    ".txt": "ri-file-text-line",
    ".md": "ri-markdown-line",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/{document_id}/upload")
async def upload_file(
    document_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a file (images, PDFs, CSVs, etc.) for a document."""
    # Verify document access
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not PermissionService.check_permission(db, current_user.id, "write", "document", document_id):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Check file extension
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not allowed. Allowed types: images, PDF, CSV, JSON, etc.")
    
    # Read content and check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum 50MB allowed.")
    
    # Generate unique filename
    unique_name = f"{uuid_lib.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / unique_name
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Determine file type
    is_image = ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
    icon = FILE_TYPE_ICONS.get(ext, "ri-file-line")
    
    # Return URL and metadata
    url = f"/static/uploads/{unique_name}"
    
    return {
        "url": url,
        "filename": file.filename,
        "size": len(content),
        "type": ext.lstrip("."),
        "is_image": is_image,
        "icon": icon,
    }


# ============ Helpers ============

def _document_to_response(document: Document, db: Session, user_id: str) -> DocumentResponse:
    """Convert document model to response."""
    is_fav = DocumentService.is_favorited(db, user_id, document.id)
    
    return DocumentResponse(
        id=document.id,
        workspace_id=document.workspace_id,
        project_id=document.project_id,
        parent_id=document.parent_id,
        title=document.title,
        slug=document.slug,
        content=document.content,
        content_html=document.content_html,
        summary=document.summary,
        icon=document.icon,
        metadata=dict(document.doc_metadata) if hasattr(document.doc_metadata, 'items') else {},
        status=document.status,
        visibility=document.visibility,
        owner_id=document.owner_id,
        current_version=document.current_version,
        view_count=document.view_count,
        created_at=document.created_at,
        updated_at=document.updated_at,
        published_at=document.published_at,
        is_favorited=is_fav
    )
