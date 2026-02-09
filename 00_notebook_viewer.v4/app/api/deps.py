# -*- coding: utf-8 -*-
"""
API Dependencies
- Authentication dependencies
- Database session
- Current user
"""

from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth import AuthService


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


def get_token_from_request(
    request: Request,
    oauth2_token: Optional[str] = Depends(oauth2_scheme),
    bearer_token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> Optional[str]:
    """
    Extract access token from request.
    Supports: Authorization header (Bearer), cookie
    """
    # 1. OAuth2 header
    if oauth2_token:
        return oauth2_token
    
    # 2. HTTP Bearer header
    if bearer_token:
        return bearer_token.credentials
    
    # 3. Cookie fallback
    token = request.cookies.get("access_token")
    if token:
        return token
    
    return None


def get_current_user(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user.
    Raises 401 if not authenticated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    user = AuthService.get_user_from_token(db, token)
    
    if not user:
        raise credentials_exception
    
    return user


def get_current_user_optional(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Does not raise exception.
    """
    if not token:
        return None
    
    return AuthService.get_user_from_token(db, token)


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    Raises 403 if user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current superuser.
    Raises 403 if not superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


class PermissionChecker:
    """
    Dependency class for checking permissions.
    
    Usage:
        @router.get("/documents/{doc_id}")
        def get_document(
            doc_id: str,
            _: bool = Depends(PermissionChecker("read", "document"))
        ):
            ...
    """
    
    def __init__(self, permission: str, resource_type: str):
        self.permission = permission
        self.resource_type = resource_type
    
    def __call__(
        self,
        resource_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> bool:
        from app.services.permission import PermissionService
        
        if not PermissionService.check_permission(
            db,
            current_user.id,
            self.permission,
            self.resource_type,
            resource_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {self.permission} on {self.resource_type}"
            )
        
        return True


def get_client_ip(request: Request) -> Optional[str]:
    """Extract client IP from request."""
    # Check X-Forwarded-For header
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to client host
    if request.client:
        return request.client.host
    
    return None


def get_user_agent(request: Request) -> Optional[str]:
    """Extract user agent from request."""
    return request.headers.get("User-Agent")
