# -*- coding: utf-8 -*-
"""
Audit Service
- Action logging
- Change tracking
- Security events
"""

from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlalchemy.orm import Session

from app.models.audit import AuditLog, AuditAction


class AuditService:
    """Audit logging service for security and compliance."""
    
    @classmethod
    def log(
        cls,
        db: Session,
        action: AuditAction,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        org_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Log an auditable action."""
        audit_log = AuditLog(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            user_email=user_email,
            org_id=org_id,
            workspace_id=workspace_id,
            action=action.value,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            details=details or {},
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            success=success,
            error_message=error_message,
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    
    @classmethod
    def log_login(
        cls,
        db: Session,
        user_id: str,
        user_email: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Log login attempt."""
        action = AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED
        
        return cls.log(
            db=db,
            action=action,
            user_id=user_id if success else None,
            user_email=user_email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message,
            details={"email": user_email}
        )
    
    @classmethod
    def log_document_action(
        cls,
        db: Session,
        action: AuditAction,
        document_id: str,
        document_title: str,
        user_id: str,
        user_email: str,
        workspace_id: str,
        org_id: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> AuditLog:
        """Log document-related action."""
        return cls.log(
            db=db,
            action=action,
            user_id=user_id,
            user_email=user_email,
            org_id=org_id,
            workspace_id=workspace_id,
            resource_type="document",
            resource_id=document_id,
            resource_name=document_title,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            request_id=request_id,
        )
    
    @classmethod
    def log_permission_change(
        cls,
        db: Session,
        action: AuditAction,
        target_user_id: str,
        target_user_email: str,
        changed_by_id: str,
        changed_by_email: str,
        scope_type: str,
        scope_id: str,
        old_role: Optional[str] = None,
        new_role: Optional[str] = None,
        org_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log permission/role changes."""
        return cls.log(
            db=db,
            action=action,
            user_id=changed_by_id,
            user_email=changed_by_email,
            org_id=org_id,
            resource_type="role_binding",
            resource_id=scope_id,
            details={
                "target_user_id": target_user_id,
                "target_user_email": target_user_email,
                "scope_type": scope_type,
            },
            old_values={"role": old_role} if old_role else None,
            new_values={"role": new_role} if new_role else None,
            ip_address=ip_address,
        )
    
    @classmethod
    def get_user_activity(
        cls,
        db: Session,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[AuditLog]:
        """Get recent activity for a user."""
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(
            AuditLog.timestamp.desc()
        ).offset(offset).limit(limit).all()
    
    @classmethod
    def get_resource_activity(
        cls,
        db: Session,
        resource_type: str,
        resource_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[AuditLog]:
        """Get recent activity for a resource."""
        return db.query(AuditLog).filter(
            AuditLog.resource_type == resource_type,
            AuditLog.resource_id == resource_id
        ).order_by(
            AuditLog.timestamp.desc()
        ).offset(offset).limit(limit).all()
    
    @classmethod
    def get_workspace_activity(
        cls,
        db: Session,
        workspace_id: str,
        limit: int = 50,
        offset: int = 0,
        action_filter: Optional[List[str]] = None
    ) -> List[AuditLog]:
        """Get recent activity in a workspace."""
        query = db.query(AuditLog).filter(
            AuditLog.workspace_id == workspace_id
        )
        
        if action_filter:
            query = query.filter(AuditLog.action.in_(action_filter))
        
        return query.order_by(
            AuditLog.timestamp.desc()
        ).offset(offset).limit(limit).all()
    
    @classmethod
    def get_org_activity(
        cls,
        db: Session,
        org_id: str,
        limit: int = 50,
        offset: int = 0,
        action_filter: Optional[List[str]] = None
    ) -> List[AuditLog]:
        """Get recent activity in an organization."""
        query = db.query(AuditLog).filter(
            AuditLog.org_id == org_id
        )
        
        if action_filter:
            query = query.filter(AuditLog.action.in_(action_filter))
        
        return query.order_by(
            AuditLog.timestamp.desc()
        ).offset(offset).limit(limit).all()
    
    @classmethod
    def get_security_events(
        cls,
        db: Session,
        org_id: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get security-related events (logins, permission changes, etc.)."""
        security_actions = [
            AuditAction.LOGIN.value,
            AuditAction.LOGOUT.value,
            AuditAction.LOGIN_FAILED.value,
            AuditAction.PASSWORD_CHANGED.value,
            AuditAction.PERMISSION_GRANTED.value,
            AuditAction.PERMISSION_REVOKED.value,
            AuditAction.ROLE_ASSIGNED.value,
            AuditAction.ROLE_REMOVED.value,
            AuditAction.USER_CREATED.value,
            AuditAction.USER_DELETED.value,
        ]
        
        query = db.query(AuditLog).filter(
            AuditLog.action.in_(security_actions)
        )
        
        if org_id:
            query = query.filter(AuditLog.org_id == org_id)
        
        return query.order_by(
            AuditLog.timestamp.desc()
        ).limit(limit).all()
