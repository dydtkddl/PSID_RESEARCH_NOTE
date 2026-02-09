# auth.py
# -*- coding: utf-8 -*-
"""
Cookie session auth (HMAC-signed token)
- Token payload: {"u": "<username>", "iat": <unix>, "exp": <unix>}
- Token format: <body_b64u>.<sig_b64u>
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import time
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, Response

logger = logging.getLogger("auth")


def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64u_dec(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "==")


def _get_session_cfg(config: Dict[str, Any]) -> Dict[str, Any]:
    sess = config.get("session") or {}
    secret = sess.get("secret")
    ttl = sess.get("ttl_seconds")
    if not secret or not isinstance(secret, str):
        raise RuntimeError("Config.session.secret is missing/invalid")
    if not ttl or not isinstance(ttl, int):
        raise RuntimeError("Config.session.ttl_seconds is missing/invalid")
    return sess


def make_session_token(username: str, secret: str, ttl_seconds: int) -> str:
    now = int(time.time())
    payload = {"u": username, "iat": now, "exp": now + int(ttl_seconds)}

    body = _b64u(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    sig = hmac.new(secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    token = f"{body}.{_b64u(sig)}"

    logger.info("session token issued user=%s exp=%s", username, payload["exp"])
    return token


def read_session_token(token: str, secret: str) -> Optional[Dict[str, Any]]:
    try:
        body, sig = token.split(".", 1)

        expected = hmac.new(secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64u(expected), sig):
            logger.warning("invalid token signature")
            return None

        payload = json.loads(_b64u_dec(body).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            logger.info("token expired user=%s", payload.get("u"))
            return None

        return payload

    except Exception:
        logger.exception("read_session_token failed")
        return None


def set_session_cookie(response: Response, config: Dict[str, Any], username: str) -> None:
    """
    Call this after successful login.
    """
    sess = _get_session_cfg(config)
    token = make_session_token(username, sess["secret"], sess["ttl_seconds"])

    cookie_name = sess.get("cookie_name", "session")
    samesite = sess.get("cookie_samesite", "lax")  # "lax" / "strict" / "none"
    secure = bool(sess.get("cookie_secure", False))

    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        path="/",
    )
    logger.info("session cookie set user=%s cookie=%s secure=%s samesite=%s", username, cookie_name, secure, samesite)


def clear_session_cookie(response: Response, config: Dict[str, Any]) -> None:
    sess = config.get("session") or {}
    cookie_name = sess.get("cookie_name", "session")
    response.delete_cookie(key=cookie_name, path="/")
    logger.info("session cookie cleared cookie=%s", cookie_name)


def get_current_user(request: Request, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns:
      {"username": <str>, "rule": <dict>}
    Raises:
      HTTPException(401) if not authenticated
    """
    sess = _get_session_cfg(config)
    cookie_name = sess.get("cookie_name", "session")

    token = request.cookies.get(cookie_name)
    if not token:
        logger.info("no session cookie cookie=%s", cookie_name)
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = read_session_token(token, sess["secret"])
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid session")

    username = payload.get("u")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid session payload")

    users = config.get("users") or {}
    user_rule = users.get(username)
    if not user_rule:
        logger.warning("unknown user in config user=%s", username)
        raise HTTPException(status_code=401, detail="Unknown user")

    logger.info("authenticated user=%s", username)
    return {"username": username, "rule": user_rule}
