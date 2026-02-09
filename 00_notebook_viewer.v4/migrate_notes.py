# -*- coding: utf-8 -*-
"""
Research Notes Migration Script
Imports markdown notes from folder structure into the platform database.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.organization import Organization
from app.models.workspace import Workspace
from app.models.document import Document, DocumentStatus, DocumentVisibility
from app.models.permission import Role, RoleBinding
from app.services.document import DocumentService
from app.services.security import SecurityService


# Configuration
NOTES_ROOT = r"c:\Users\user\Desktop\Reseach_Note"
TARGET_USER = {
    "email": "dydtkddhkdwk@khu.ac.kr",
    "username": "dydtkddl",
    "password": "2019101074a!@",
    "display_name": "연구원"
}

# Folders to import (each becomes a workspace)
FOLDERS_TO_IMPORT = [
    "ABN",
    "Isotherm데이터베이스",
    "KHU_챗봇",
    "MOF강화학습",
    "PSID_Dropbox",
    "QM9_전해질첨가제스크리닝",
    "SEI크롤링",
    "기타",
    "열분해크롤링",
    "올리고머_IL",
    "자율제조"
]


def create_user_if_not_exists(db: Session) -> User:
    """Create target user if doesn't exist."""
    user = db.query(User).filter(User.email == TARGET_USER["email"]).first()
    if user:
        print(f"User already exists: {user.email}")
        return user
    
    user = User(
        email=TARGET_USER["email"],
        username=TARGET_USER["username"],
        display_name=TARGET_USER["display_name"],
        password_hash=SecurityService.hash_password(TARGET_USER["password"]),
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {user.email}")
    return user


def create_organization_if_not_exists(db: Session, user: User) -> Organization:
    """Create organization for user."""
    org = db.query(Organization).filter(Organization.slug == "research-notes").first()
    if org:
        print(f"Organization already exists: {org.name}")
        return org
    
    org = Organization(
        name="연구 노트",
        slug="research-notes",
        owner_id=user.id
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    print(f"Created organization: {org.name}")
    return org




def create_workspace(db: Session, org: Organization, user: User, folder_name: str) -> Workspace:
    """Create workspace for a folder."""
    # Check if workspace exists
    slug = folder_name.lower().replace("_", "-").replace(" ", "-")
    ws = db.query(Workspace).filter(
        Workspace.org_id == org.id,
        Workspace.slug == slug
    ).first()
    
    if ws:
        print(f"  Workspace already exists: {ws.name}")
        return ws
    
    # Create workspace
    ws = Workspace(
        name=folder_name,
        slug=slug,
        org_id=org.id,
        description=f"연구 노트: {folder_name}",
        icon="📁"
    )
    db.add(ws)
    db.commit()
    db.refresh(ws)
    
    # Assign owner role to user for this workspace
    binding = RoleBinding(
        user_id=user.id,
        role="owner",  # RoleType value as string
        scope_type="workspace",
        workspace_id=ws.id,
        is_active=True
    )
    db.add(binding)
    db.commit()
    
    print(f"  Created workspace: {ws.name}")
    return ws


def import_document(db: Session, ws: Workspace, user: User, file_path: Path, folder_name: str) -> Document:
    """Import a markdown file as a document."""
    import re
    import uuid
    import markdown
    from urllib.parse import quote
    
    # Skip non-markdown files
    if file_path.suffix.lower() != ".md":
        return None
    
    # Read content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"    Error reading {file_path}: {e}")
        return None
    
    # Title from filename
    title = file_path.stem
    
    # Check if document already exists
    existing = db.query(Document).filter(
        Document.workspace_id == ws.id,
        Document.title == title
    ).first()
    
    if existing:
        print(f"    Document already exists: {title}")
        return existing
    
    # Convert relative image paths to absolute /notes/ URLs
    # Match patterns like: ![alt](image.png), ![alt](imgs/image.png), ![alt](image-1.png)
    def fix_image_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # Skip URLs (http://, https://, //)
        if img_path.startswith(('http://', 'https://', '//')):
            return match.group(0)
        # Skip already absolute paths
        if img_path.startswith('/'):
            return match.group(0)
        # Convert to /notes/folder_name/image_path (URL-encoded for Korean)
        encoded_folder = quote(folder_name, safe='')
        encoded_img = quote(img_path, safe='/')
        new_path = f"/notes/{encoded_folder}/{encoded_img}"
        return f"![{alt_text}]({new_path})"
    
    content_fixed = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, content)
    
    # Generate slug from title
    slug = re.sub(r'[^a-zA-Z0-9가-힣\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug)[:100]
    
    # Render markdown to HTML
    try:
        content_html = markdown.markdown(content_fixed, extensions=['tables', 'fenced_code', 'toc'])
    except:
        content_html = f"<pre>{content_fixed}</pre>"
    
    # Create document directly
    doc = Document(
        id=str(uuid.uuid4()),
        workspace_id=ws.id,
        title=title,
        slug=slug,
        content=content_fixed,
        content_html=content_html,
        icon="📄",
        status=DocumentStatus.PUBLISHED,
        visibility=DocumentVisibility.WORKSPACE,
        owner_id=user.id,
        current_version=1,
        view_count=0,
        published_at=datetime.utcnow()
    )
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    print(f"    Imported: {title[:50]}...")
    return doc


def import_folder(db: Session, org: Organization, user: User, folder_name: str):
    """Import a folder as a workspace with its documents."""
    folder_path = Path(NOTES_ROOT) / folder_name
    
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return
    
    print(f"\nImporting folder: {folder_name}")
    
    # Create workspace
    ws = create_workspace(db, org, user, folder_name)
    
    # Find all markdown files
    md_files = list(folder_path.glob("*.md"))
    print(f"  Found {len(md_files)} markdown files")
    
    # Import each file
    imported = 0
    for md_file in md_files:
        doc = import_document(db, ws, user, md_file, folder_name)
        if doc:
            imported += 1
    
    print(f"  Imported {imported} documents to {folder_name}")


def main():
    """Main migration function."""
    print("=" * 60)
    print("Research Notes Migration")
    print("=" * 60)
    
    # Create tables if needed
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create user
        user = create_user_if_not_exists(db)
        
        # Create organization
        org = create_organization_if_not_exists(db, user)
        
        # Import each folder
        for folder_name in FOLDERS_TO_IMPORT:
            import_folder(db, org, user, folder_name)
        
        print("\n" + "=" * 60)
        print("Migration complete!")
        print("=" * 60)
        print(f"\nLogin credentials:")
        print(f"  Email: {TARGET_USER['email']}")
        print(f"  Password: {TARGET_USER['password']}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
