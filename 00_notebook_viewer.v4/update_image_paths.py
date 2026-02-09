# -*- coding: utf-8 -*-
"""
Update existing documents to fix image paths.
"""

import os
import sys
import re
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.document import Document
from app.models.workspace import Workspace
import markdown


def fix_image_paths(content: str, folder_name: str) -> str:
    """Convert relative image paths to absolute /notes/ URLs."""
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
    
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, content)


def main():
    """Update all documents to fix image paths."""
    print("=" * 60)
    print("Updating Document Image Paths")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Get all workspaces with their documents
        workspaces = db.query(Workspace).all()
        
        updated_count = 0
        for ws in workspaces:
            folder_name = ws.name
            print(f"\nWorkspace: {folder_name}")
            
            # Get documents in this workspace
            docs = db.query(Document).filter(Document.workspace_id == ws.id).all()
            
            for doc in docs:
                # Fix image paths in content
                if doc.content:
                    fixed_content = fix_image_paths(doc.content, folder_name)
                    
                    if fixed_content != doc.content:
                        # Update document
                        doc.content = fixed_content
                        
                        # Re-render HTML
                        try:
                            doc.content_html = markdown.markdown(
                                fixed_content, 
                                extensions=['tables', 'fenced_code', 'toc']
                            )
                        except:
                            doc.content_html = f"<pre>{fixed_content}</pre>"
                        
                        db.commit()
                        updated_count += 1
                        print(f"  Updated: {doc.title[:50]}...")
        
        print(f"\n{'=' * 60}")
        print(f"Updated {updated_count} documents")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
