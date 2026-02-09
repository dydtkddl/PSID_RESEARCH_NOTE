# security.py
# -*- coding: utf-8 -*-
"""
Password hashing & verification (PBKDF2-HMAC-SHA256)
- Store only password_hash in Config.json
- Format: pbkdf2_sha256$<iterations>$<salt_b64u>$<dk_b64u>
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
from typing import Optional

logger = logging.getLogger("security")

DEFAULT_PBKDF2_ITER = 200_000
SALT_BYTES = 16


def _b64u_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64u_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "==")


def hash_password(
    password: str,
    *,
    iterations: int = DEFAULT_PBKDF2_ITER,
    salt: Optional[bytes] = None,
) -> str:
    """
    Generate PBKDF2-HMAC-SHA256 password hash string.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    if salt is None:
        salt = os.urandom(SALT_BYTES)

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        int(iterations),
    )

    out = f"pbkdf2_sha256${int(iterations)}${_b64u_encode(salt)}${_b64u_encode(dk)}"
    logger.info("password hash generated (iterations=%s, salt_bytes=%s)", iterations, len(salt))
    return out


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify password against stored PBKDF2 hash string.
    """
    try:
        if not password or not stored_hash:
            return False

        algo, it_s, salt_s, dk_s = stored_hash.split("$", 3)
        if algo != "pbkdf2_sha256":
            logger.warning("unsupported algo: %s", algo)
            return False

        iterations = int(it_s)
        salt = _b64u_decode(salt_s)
        expected = _b64u_decode(dk_s)

        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        ok = hmac.compare_digest(dk, expected)
        logger.info("password verify result=%s (iterations=%s)", ok, iterations)
        return ok

    except Exception:
        logger.exception("verify_password failed")
        return False
