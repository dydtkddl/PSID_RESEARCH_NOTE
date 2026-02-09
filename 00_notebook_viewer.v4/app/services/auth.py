# -*- coding: utf-8 -*-
"""
Authentication Service
- JWT token management (Access + Refresh)
- User authentication
- Session management
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User, RefreshToken
from app.services.security import SecurityService


class AuthService:
    """Authentication and authorization service."""
    
    @classmethod
    def create_access_token(
        cls,
        user_id: str,
        email: str,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create JWT access token."""
        now = datetime.utcnow()
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "sub": user_id,
            "email": email,
            "type": "access",
            "iat": now,
            "exp": expire,
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
    
    @classmethod
    def create_refresh_token(
        cls,
        db: Session,
        user_id: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[str, RefreshToken]:
        """
        Create refresh token and store in database.
        Returns (raw_token, refresh_token_model)
        """
        raw_token = SecurityService.generate_token(48)
        token_hash = SecurityService.hash_token(raw_token)
        
        expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires_at,
        )
        
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        
        return raw_token, refresh_token
    
    @classmethod
    def verify_access_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode access token."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            if payload.get("type") != "access":
                return None
            
            return payload
        
        except JWTError:
            return None
    
    @classmethod
    def verify_refresh_token(cls, db: Session, raw_token: str) -> Optional[RefreshToken]:
        """Verify refresh token and return the model if valid."""
        token_hash = SecurityService.hash_token(raw_token)
        
        refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        return refresh_token
    
    @classmethod
    def rotate_refresh_token(
        cls,
        db: Session,
        old_token: RefreshToken,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[str, RefreshToken]:
        """
        Rotate refresh token (revoke old, create new).
        Returns (new_raw_token, new_refresh_token_model)
        """
        # Revoke old token
        old_token.revoked = True
        old_token.revoked_at = datetime.utcnow()
        db.add(old_token)
        
        # Create new token
        new_raw_token, new_refresh_token = cls.create_refresh_token(
            db,
            old_token.user_id,
            device_info=device_info or old_token.device_info,
            ip_address=ip_address or old_token.ip_address
        )
        
        return new_raw_token, new_refresh_token
    
    @classmethod
    def revoke_refresh_token(cls, db: Session, token_hash: str) -> bool:
        """Revoke a specific refresh token."""
        refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash
        ).first()
        
        if refresh_token:
            refresh_token.revoked = True
            refresh_token.revoked_at = datetime.utcnow()
            db.commit()
            return True
        
        return False
    
    @classmethod
    def revoke_all_user_tokens(cls, db: Session, user_id: str) -> int:
        """Revoke all refresh tokens for a user. Returns count revoked."""
        now = datetime.utcnow()
        
        count = db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        ).update({
            RefreshToken.revoked: True,
            RefreshToken.revoked_at: now
        })
        
        db.commit()
        return count
    
    @classmethod
    def authenticate_user(
        cls,
        db: Session,
        email_or_username: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user with email/username and password."""
        # Try to find user by email or username
        user = db.query(User).filter(
            (User.email == email_or_username) | 
            (User.username == email_or_username)
        ).first()
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not SecurityService.verify_password(password, user.password_hash):
            return None
        
        return user
    
    @classmethod
    def login(
        cls,
        db: Session,
        email_or_username: str,
        password: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Full login flow: authenticate and generate tokens.
        Returns dict with access_token, refresh_token, and user info.
        """
        user = cls.authenticate_user(db, email_or_username, password)
        
        if not user:
            return None
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        db.add(user)
        
        # Generate tokens
        access_token = cls.create_access_token(user.id, user.email)
        refresh_token_raw, _ = cls.create_refresh_token(
            db,
            user.id,
            device_info=device_info,
            ip_address=ip_address
        )
        
        db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_raw,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "display_name": user.display_name,
                "is_superuser": user.is_superuser,
            }
        }
    
    @classmethod
    def refresh_tokens(
        cls,
        db: Session,
        refresh_token_raw: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Refresh access token using refresh token.
        Implements token rotation for security.
        """
        old_token = cls.verify_refresh_token(db, refresh_token_raw)
        
        if not old_token:
            return None
        
        # Get user
        user = db.query(User).filter(User.id == old_token.user_id).first()
        
        if not user or not user.is_active:
            return None
        
        # Rotate tokens
        new_refresh_raw, _ = cls.rotate_refresh_token(
            db,
            old_token,
            device_info=device_info,
            ip_address=ip_address
        )
        
        # Create new access token
        access_token = cls.create_access_token(user.id, user.email)
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_raw,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    
    @classmethod
    def logout(cls, db: Session, refresh_token_raw: str) -> bool:
        """Logout by revoking refresh token."""
        token_hash = SecurityService.hash_token(refresh_token_raw)
        return cls.revoke_refresh_token(db, token_hash)
    
    @classmethod
    def get_user_from_token(cls, db: Session, access_token: str) -> Optional[User]:
        """Get user from access token."""
        payload = cls.verify_access_token(access_token)
        
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
        
        return user
