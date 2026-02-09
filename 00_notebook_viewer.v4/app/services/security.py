# -*- coding: utf-8 -*-
"""
Security Service
- Password hashing (PBKDF2)
- Token generation
- Input sanitization
"""

import base64
import hashlib
import hmac
import os
import re
import secrets
from typing import Optional
import bleach

from app.config import settings


class SecurityService:
    """Security utilities for the application."""
    
    # PBKDF2 settings
    ITERATIONS = settings.PBKDF2_ITERATIONS
    SALT_BYTES = 16
    HASH_BYTES = 32
    
    # Bleach settings for HTML sanitization
    ALLOWED_TAGS = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'dd', 'del',
        'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i',
        'img', 'ins', 'kbd', 'li', 'ol', 'p', 'pre', 'q', 's', 'samp', 'small',
        'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
        'thead', 'tr', 'u', 'ul', 'details', 'summary', 'mark', 'figure', 
        'figcaption', 'video', 'audio', 'source', 'iframe',
        # MathJax
        'mjx-container', 'mjx-math', 'mjx-mrow', 'mjx-mi', 'mjx-mo', 'mjx-mn',
        'mjx-msup', 'mjx-msub', 'mjx-mfrac', 'mjx-sqrt', 'mjx-root',
        'svg', 'path', 'g', 'rect', 'circle', 'line', 'use', 'defs',
    ]
    
    ALLOWED_ATTRS = {
        '*': ['class', 'id', 'style', 'data-*'],
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height', 'loading'],
        'video': ['src', 'controls', 'width', 'height', 'poster'],
        'audio': ['src', 'controls'],
        'source': ['src', 'type'],
        'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'],
        'td': ['colspan', 'rowspan', 'align'],
        'th': ['colspan', 'rowspan', 'align', 'scope'],
        'svg': ['viewBox', 'width', 'height', 'xmlns', 'fill', 'stroke'],
        'path': ['d', 'fill', 'stroke', 'stroke-width'],
    }
    
    @classmethod
    def _b64_encode(cls, data: bytes) -> str:
        """URL-safe base64 encode."""
        return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')
    
    @classmethod
    def _b64_decode(cls, s: str) -> bytes:
        """URL-safe base64 decode."""
        padding = 4 - (len(s) % 4)
        if padding != 4:
            s += '=' * padding
        return base64.urlsafe_b64decode(s)
    
    @classmethod
    def hash_password(cls, password: str, salt: Optional[bytes] = None) -> str:
        """
        Hash password using PBKDF2-HMAC-SHA256.
        
        Returns: pbkdf2_sha256$<iterations>$<salt_b64>$<hash_b64>
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        if salt is None:
            salt = os.urandom(cls.SALT_BYTES)
        
        dk = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            cls.ITERATIONS,
            dklen=cls.HASH_BYTES
        )
        
        return f"pbkdf2_sha256${cls.ITERATIONS}${cls._b64_encode(salt)}${cls._b64_encode(dk)}"
    
    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            if not password or not password_hash:
                return False
            
            parts = password_hash.split('$')
            if len(parts) != 4 or parts[0] != 'pbkdf2_sha256':
                return False
            
            iterations = int(parts[1])
            salt = cls._b64_decode(parts[2])
            expected_hash = cls._b64_decode(parts[3])
            
            dk = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                iterations,
                dklen=len(expected_hash)
            )
            
            return hmac.compare_digest(dk, expected_hash)
        
        except Exception:
            return False
    
    @classmethod
    def generate_token(cls, length: int = 32) -> str:
        """Generate cryptographically secure random token."""
        return secrets.token_urlsafe(length)
    
    @classmethod
    def hash_token(cls, token: str) -> str:
        """Hash a token for storage (one-way)."""
        return hashlib.sha256(token.encode()).hexdigest()
    
    @classmethod
    def generate_password(cls, length: int = 16) -> str:
        """Generate a random password."""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @classmethod
    def sanitize_html(cls, html: str) -> str:
        """Sanitize HTML to prevent XSS attacks."""
        if not html:
            return ""
        
        return bleach.clean(
            html,
            tags=cls.ALLOWED_TAGS,
            attributes=cls.ALLOWED_ATTRS,
            strip=True
        )
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        if not filename:
            return "unnamed"
        
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Remove null bytes and other dangerous characters
        filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
        
        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename or "unnamed"
    
    @classmethod
    def generate_slug(cls, text: str) -> str:
        """Generate URL-safe slug from text."""
        if not text:
            return secrets.token_hex(4)
        
        # Convert to lowercase
        slug = text.lower()
        
        # Replace spaces and special chars with hyphens
        slug = re.sub(r'[^\w\s가-힣-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = slug.strip('-')
        
        # Limit length
        if len(slug) > 100:
            slug = slug[:100].rsplit('-', 1)[0]
        
        return slug or secrets.token_hex(4)
