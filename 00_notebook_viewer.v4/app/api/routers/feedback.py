# -*- coding: utf-8 -*-
"""
Feedback & Help API Router
"""

import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer

from app.database import get_db, Base
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(tags=["feedback"])


# ============ Feedback Model ============

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    user_email = Column(String(255), nullable=True)
    type = Column(String(20), default="general")  # bug, feature, general, other
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5
    status = Column(String(20), default="open")  # open, in_progress, resolved, closed
    admin_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============ Schemas ============

class FeedbackCreate(BaseModel):
    type: str = "general"
    title: str
    message: str
    rating: Optional[int] = None


class FeedbackResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    rating: Optional[int]
    status: str
    admin_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Help Content ============

HELP_SECTIONS = [
    {
        "id": "getting-started",
        "title": "시작하기",
        "icon": "ri-rocket-line",
        "items": [
            {
                "title": "플랫폼 소개",
                "content": "Research Platform은 PSID LAB의 연구 노트 관리 플랫폼입니다. Markdown 기반의 강력한 에디터, 실시간 협업, PDF 내보내기 등 다양한 기능을 제공합니다.",
            },
            {
                "title": "첫 문서 만들기",
                "content": "대시보드에서 '새 문서' 버튼을 클릭하거나, 워크스페이스 페이지에서 문서를 생성할 수 있습니다. 빈 문서, 회의록, 실험 노트 템플릿을 선택할 수 있습니다.",
            },
            {
                "title": "워크스페이스 관리",
                "content": "워크스페이스는 문서를 그룹으로 관리하는 공간입니다. 사이드바에서 '+' 버튼으로 새 워크스페이스를 만들 수 있습니다.",
            },
        ],
    },
    {
        "id": "editor",
        "title": "에디터 사용법",
        "icon": "ri-edit-line",
        "items": [
            {
                "title": "Markdown 문법",
                "content": "# 제목, ## 부제목, **굵게**, *기울임*, `코드`, > 인용, - 목록 등 표준 Markdown 문법을 지원합니다.",
            },
            {
                "title": "수식 입력",
                "content": "LaTeX 수식을 $..$ (인라인) 또는 $$...$$ (블록) 으로 입력할 수 있습니다. 예: $E = mc^2$",
            },
            {
                "title": "이미지 & 파일 첨부",
                "content": "에디터 툴바의 이미지 버튼을 클릭하거나, 파일을 직접 드래그 앤 드롭할 수 있습니다. PNG, JPG, PDF, CSV 등 다양한 형식을 지원합니다.",
            },
            {
                "title": "실시간 협업",
                "content": "같은 문서를 여러 사람이 동시에 편집할 수 있습니다. 다른 사용자의 커서와 선택 영역이 실시간으로 표시됩니다.",
            },
        ],
    },
    {
        "id": "shortcuts",
        "title": "키보드 단축키",
        "icon": "ri-keyboard-line",
        "items": [
            {"title": "Ctrl+B", "content": "굵게"},
            {"title": "Ctrl+I", "content": "기울임"},
            {"title": "Ctrl+K", "content": "링크 삽입 / 명령 팔레트"},
            {"title": "Ctrl+S", "content": "저장"},
            {"title": "Tab", "content": "들여쓰기"},
            {"title": "Ctrl+Z", "content": "실행 취소"},
            {"title": "Ctrl+Shift+Z", "content": "다시 실행"},
        ],
    },
    {
        "id": "export",
        "title": "내보내기",
        "icon": "ri-download-line",
        "items": [
            {
                "title": "PDF 내보내기",
                "content": "문서 뷰어의 '더보기' 메뉴에서 'PDF로 내보내기'를 선택하면 Playwright 기반의 고품질 PDF가 생성됩니다.",
            },
            {
                "title": "Markdown 다운로드",
                "content": "'마크다운 다운로드'를 선택하면 원본 Markdown 파일을 내려받을 수 있습니다.",
            },
        ],
    },
    {
        "id": "collaboration",
        "title": "팀 협업",
        "icon": "ri-team-line",
        "items": [
            {
                "title": "멤버 초대",
                "content": "워크스페이스 설정에서 초대 링크를 생성하여 팀원을 초대할 수 있습니다. Viewer, Editor, Admin 역할을 선택할 수 있습니다.",
            },
            {
                "title": "댓글 & 하이라이트",
                "content": "문서 뷰어에서 텍스트를 선택하면 하이라이트나 댓글을 추가할 수 있습니다.",
            },
        ],
    },
]

KEYBOARD_SHORTCUTS = [
    {"keys": ["Ctrl", "B"], "description": "굵게"},
    {"keys": ["Ctrl", "I"], "description": "기울임"},
    {"keys": ["Ctrl", "K"], "description": "링크 삽입"},
    {"keys": ["Ctrl", "S"], "description": "저장"},
    {"keys": ["Ctrl", "Z"], "description": "실행 취소"},
    {"keys": ["Ctrl", "Shift", "Z"], "description": "다시 실행"},
    {"keys": ["Tab"], "description": "들여쓰기"},
    {"keys": ["Ctrl", "/"], "description": "명령 팔레트"},
]


# ============ API Endpoints ============

@router.get("/api/v1/help")
async def get_help_content():
    """Get all help content sections."""
    return {
        "sections": HELP_SECTIONS,
        "shortcuts": KEYBOARD_SHORTCUTS,
    }


@router.get("/api/v1/help/{section_id}")
async def get_help_section(section_id: str):
    """Get a specific help section."""
    for section in HELP_SECTIONS:
        if section["id"] == section_id:
            return section
    raise HTTPException(status_code=404, detail="Help section not found")


@router.post("/api/v1/feedback", response_model=FeedbackResponse)
async def create_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Submit user feedback."""
    feedback = Feedback(
        user_id=current_user.id,
        user_email=current_user.email,
        type=data.type,
        title=data.title,
        message=data.message,
        rating=data.rating,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/api/v1/feedback", response_model=List[FeedbackResponse])
async def list_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 20,
):
    """List user's own feedback."""
    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.user_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .limit(limit)
        .all()
    )
    return feedbacks


@router.get("/api/v1/feedback/all", response_model=List[FeedbackResponse])
async def list_all_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 50,
):
    """List all feedback (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    feedbacks = (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .limit(limit)
        .all()
    )
    return feedbacks
