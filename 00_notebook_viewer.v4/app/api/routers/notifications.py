# -*- coding: utf-8 -*-
"""
Notifications API Router
- Get user notifications
- Mark as read
- Delete notifications
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.api.deps import get_current_active_user


router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    link: str | None
    is_read: bool
    created_at: datetime


@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    limit: int = 20,
    unread_only: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user notifications."""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    return [
        NotificationResponse(
            id=n.id,
            type=n.type,
            title=n.title,
            message=n.message,
            link=n.link,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in notifications
    ]


@router.get("/count")
def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get unread notifications count."""
    count = db.query(func.count(Notification.id)).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).scalar() or 0
    
    return {"count": count}


@router.post("/{notification_id}/read")
def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Marked as read"}


@router.post("/read-all")
def mark_all_as_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read."""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({
        Notification.is_read: True,
        Notification.read_at: datetime.utcnow()
    })
    db.commit()
    
    return {"message": "All notifications marked as read"}


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a notification."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted"}
