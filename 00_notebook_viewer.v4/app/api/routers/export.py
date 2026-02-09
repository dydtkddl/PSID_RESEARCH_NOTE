# -*- coding: utf-8 -*-
"""
PDF Export Router - Playwright-based PDF generation
"""

import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user
from app.services.document import DocumentService
from app.services.permission import PermissionService

router = APIRouter(prefix="/export", tags=["export"])


async def generate_pdf_from_html(html_content: str, title: str = "Document") -> bytes:
    """Generate PDF from HTML using Playwright."""
    from playwright.async_api import async_playwright

    full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #1a1a2e;
            line-height: 1.8;
            padding: 40px 60px;
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{ font-size: 2rem; font-weight: 700; margin: 1.5em 0 0.5em; border-bottom: 2px solid #3B82A0; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5rem; font-weight: 600; margin: 1.3em 0 0.4em; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.25rem; font-weight: 600; margin: 1.2em 0 0.3em; }}
        p {{ margin-bottom: 1em; }}
        code {{ font-family: 'Fira Code', monospace; background: #f3f4f6; padding: 0.2em 0.4em; border-radius: 4px; font-size: 0.875em; }}
        pre {{ background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 1em 0; }}
        pre code {{ background: none; padding: 0; color: inherit; }}
        blockquote {{ border-left: 4px solid #3B82A0; padding-left: 16px; margin: 1em 0; color: #6b7280; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1em 0; }}
        th, td {{ border: 1px solid #e5e7eb; padding: 10px 14px; text-align: left; }}
        th {{ background: #f9fafb; font-weight: 600; }}
        img {{ max-width: 100%; }}
        ul, ol {{ padding-left: 2em; margin: 1em 0; }}
        li {{ margin: 0.3em 0; }}
        hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 2em 0; }}
        .pdf-header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #3B82A0; }}
        .pdf-header h1 {{ border: none; margin: 0; font-size: 1.8rem; color: #3B82A0; }}
        .pdf-header .meta {{ color: #6b7280; font-size: 0.875rem; margin-top: 8px; }}
        .pdf-footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 0.75rem; }}
    </style>
</head>
<body>
    <div class="pdf-header">
        <h1>{title}</h1>
        <div class="meta">PSID LAB Research Platform &middot; Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    <div class="content">
        {html_content}
    </div>
    <div class="pdf-footer">
        &copy; {datetime.now().year} PSID LAB &middot; Research Platform
    </div>
</body>
</html>"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(full_html, wait_until="networkidle")
        await asyncio.sleep(0.5)  # Wait for fonts/styles

        pdf_bytes = await page.pdf(
            format="A4",
            margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
            print_background=True,
        )
        await browser.close()
        return pdf_bytes


@router.get("/documents/{document_id}/pdf")
async def export_document_pdf(
    document_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Export document as PDF using Playwright."""
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")

    html_content = document.content_html or ""
    title = document.title or "Untitled"

    try:
        pdf_bytes = await generate_pdf_from_html(html_content, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    safe_filename = quote(f"{title}.pdf", safe='')
    ascii_filename = title.encode('ascii', 'replace').decode() + '.pdf'

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=\"{ascii_filename}\"; filename*=UTF-8''{safe_filename}",
            "Content-Length": str(len(pdf_bytes)),
        },
    )


@router.get("/documents/{document_id}/markdown")
async def export_document_markdown(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Export document as Markdown file."""
    document = DocumentService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not PermissionService.can_read(db, current_user.id, document):
        raise HTTPException(status_code=403, detail="Permission denied")

    content = document.content or ""
    title = document.title or "Untitled"
    safe_filename = quote(f"{title}.md", safe='')
    ascii_filename = title.encode('ascii', 'replace').decode() + '.md'

    return StreamingResponse(
        iter([content.encode("utf-8")]),
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=\"{ascii_filename}\"; filename*=UTF-8''{safe_filename}",
        },
    )
