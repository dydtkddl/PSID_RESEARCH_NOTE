# -*- coding: utf-8 -*-
"""
WebSocket Real-Time Collaboration Router
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.services.auth import AuthService

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time collaboration."""

    def __init__(self):
        # document_id -> set of (websocket, user_info)
        self.active_connections: Dict[str, Set] = {}
        self.user_cursors: Dict[str, Dict[str, dict]] = {}  # doc_id -> {user_id: cursor_info}

    async def connect(self, websocket: WebSocket, document_id: str, user_info: dict):
        await websocket.accept()
        if document_id not in self.active_connections:
            self.active_connections[document_id] = set()
            self.user_cursors[document_id] = {}

        self.active_connections[document_id].add((websocket, json.dumps(user_info)))
        self.user_cursors[document_id][user_info["id"]] = {
            "name": user_info["name"],
            "color": user_info.get("color", "#3B82A0"),
            "cursor": None,
        }

        # Notify others about new user
        await self.broadcast(document_id, {
            "type": "user_joined",
            "user": user_info,
            "active_users": self._get_active_users(document_id),
            "timestamp": datetime.utcnow().isoformat(),
        }, exclude=websocket)

        # Send current state to new user
        await websocket.send_json({
            "type": "connection_established",
            "active_users": self._get_active_users(document_id),
            "timestamp": datetime.utcnow().isoformat(),
        })

    def disconnect(self, websocket: WebSocket, document_id: str, user_info: dict):
        if document_id in self.active_connections:
            to_remove = None
            for conn in self.active_connections[document_id]:
                if conn[0] == websocket:
                    to_remove = conn
                    break
            if to_remove:
                self.active_connections[document_id].discard(to_remove)

            if user_info["id"] in self.user_cursors.get(document_id, {}):
                del self.user_cursors[document_id][user_info["id"]]

            if not self.active_connections[document_id]:
                del self.active_connections[document_id]
                if document_id in self.user_cursors:
                    del self.user_cursors[document_id]

    async def broadcast(self, document_id: str, message: dict, exclude: WebSocket = None):
        if document_id not in self.active_connections:
            return
        disconnected = []
        for ws, _ in self.active_connections[document_id]:
            if ws == exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append((ws, _))
        for conn in disconnected:
            self.active_connections[document_id].discard(conn)

    def _get_active_users(self, document_id: str) -> list:
        users = []
        if document_id in self.active_connections:
            for _, user_json in self.active_connections[document_id]:
                users.append(json.loads(user_json))
        return users

    def get_collaborator_count(self, document_id: str) -> int:
        return len(self.active_connections.get(document_id, set()))


manager = ConnectionManager()

# Color palette for collaborators
COLLAB_COLORS = [
    "#3B82A0", "#7CB342", "#E91E63", "#FF9800",
    "#9C27B0", "#00BCD4", "#795548", "#607D8B",
]


def _get_user_color(user_id: str) -> str:
    hash_val = sum(ord(c) for c in user_id)
    return COLLAB_COLORS[hash_val % len(COLLAB_COLORS)]


@router.websocket("/ws/documents/{document_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    document_id: str,
    token: str = Query(None),
):
    """WebSocket endpoint for real-time document collaboration."""
    # Authenticate
    db = SessionLocal()
    user = None
    try:
        if token:
            user = AuthService.get_user_from_token(db, token)
    except Exception:
        pass
    finally:
        db.close()

    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    user_info = {
        "id": user.id,
        "name": user.display_name or user.username,
        "avatar": user.avatar_url,
        "color": _get_user_color(user.id),
    }

    await manager.connect(websocket, document_id, user_info)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "")

            if msg_type == "content_update":
                await manager.broadcast(document_id, {
                    "type": "content_update",
                    "user": user_info,
                    "content": data.get("content", ""),
                    "title": data.get("title", ""),
                    "timestamp": datetime.utcnow().isoformat(),
                }, exclude=websocket)

            elif msg_type == "cursor_update":
                if document_id in manager.user_cursors:
                    manager.user_cursors[document_id][user.id] = {
                        "name": user_info["name"],
                        "color": user_info["color"],
                        "cursor": data.get("cursor"),
                    }
                await manager.broadcast(document_id, {
                    "type": "cursor_update",
                    "user": user_info,
                    "cursor": data.get("cursor"),
                    "timestamp": datetime.utcnow().isoformat(),
                }, exclude=websocket)

            elif msg_type == "selection_update":
                await manager.broadcast(document_id, {
                    "type": "selection_update",
                    "user": user_info,
                    "selection": data.get("selection"),
                    "timestamp": datetime.utcnow().isoformat(),
                }, exclude=websocket)

            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, document_id, user_info)
        await manager.broadcast(document_id, {
            "type": "user_left",
            "user": user_info,
            "active_users": manager._get_active_users(document_id),
            "timestamp": datetime.utcnow().isoformat(),
        })
    except Exception:
        manager.disconnect(websocket, document_id, user_info)
        await manager.broadcast(document_id, {
            "type": "user_left",
            "user": user_info,
            "active_users": manager._get_active_users(document_id),
            "timestamp": datetime.utcnow().isoformat(),
        })
