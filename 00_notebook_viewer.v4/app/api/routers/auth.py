# -*- coding: utf-8 -*-
"""
Authentication API Router
- Login/Logout
- Token refresh
- Registration
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.security import SecurityService
from app.services.audit import AuditService
from app.models.audit import AuditAction
from app.api.schemas import (
    LoginRequest, LoginResponse, TokenResponse, 
    RefreshTokenRequest, UserCreate, UserResponse, MessageResponse
)
from app.api.deps import (
    get_current_user, get_current_active_user, 
    get_client_ip, get_user_agent
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    request: Request,
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login with email/username and password.
    Returns JWT tokens.
    """
    ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    result = AuthService.login(
        db,
        data.email_or_username,
        data.password,
        device_info=user_agent,
        ip_address=ip
    )
    
    if not result:
        # Log failed attempt
        AuditService.log_login(
            db,
            user_id=None,
            user_email=data.email_or_username,
            ip_address=ip,
            user_agent=user_agent,
            success=False,
            error_message="Invalid credentials"
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password"
        )
    
    # Log successful login
    AuditService.log_login(
        db,
        user_id=result["user"]["id"],
        user_email=result["user"]["email"],
        ip_address=ip,
        user_agent=user_agent,
        success=True
    )
    
    # Set cookie for browser clients
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=result["expires_in"]
    )
    
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=7 * 24 * 3600  # 7 days
    )
    
    return LoginResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        expires_in=result["expires_in"],
        user=UserResponse(
            id=result["user"]["id"],
            email=result["user"]["email"],
            username=result["user"]["username"],
            display_name=result["user"]["display_name"],
            avatar_url=None,
            theme="light",
            is_superuser=result["user"]["is_superuser"],
            created_at=None  # Will be populated from DB if needed
        )
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    Implements token rotation.
    """
    ip = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    result = AuthService.refresh_tokens(
        db,
        data.refresh_token,
        device_info=user_agent,
        ip_address=ip
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Update cookies
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=result["expires_in"]
    )
    
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 3600
    )
    
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        expires_in=result["expires_in"]
    )


@router.post("/logout", response_model=MessageResponse)
def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Logout current user.
    Revokes refresh token.
    """
    # Get refresh token from cookie or body
    refresh_token = request.cookies.get("refresh_token")
    
    if refresh_token:
        AuthService.logout(db, refresh_token)
    
    # Log logout
    AuditService.log(
        db,
        action=AuditAction.LOGOUT,
        user_id=current_user.id,
        user_email=current_user.email,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return MessageResponse(message="Successfully logged out")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    from app.config import settings
    
    if not settings.ENABLE_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Registration is disabled"
        )
    
    # Check if email exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = User(
        email=data.email,
        username=data.username,
        password_hash=SecurityService.hash_password(data.password),
        display_name=data.display_name or data.username,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Log
    AuditService.log(
        db,
        action=AuditAction.USER_CREATED,
        user_id=user.id,
        user_email=user.email,
        resource_type="user",
        resource_id=user.id,
        resource_name=user.username,
    )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        theme=user.theme,
        is_superuser=user.is_superuser,
        created_at=user.created_at
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        display_name=current_user.display_name,
        avatar_url=current_user.avatar_url,
        theme=current_user.theme,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at
    )


@router.post("/logout-all", response_model=MessageResponse)
def logout_all_sessions(
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Logout from all sessions.
    Revokes all refresh tokens for current user.
    """
    count = AuthService.revoke_all_user_tokens(db, current_user.id)
    
    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return MessageResponse(message=f"Logged out from {count} sessions")
