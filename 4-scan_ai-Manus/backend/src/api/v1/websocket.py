"""
FILE: backend/src/api/v1/websocket.py | PURPOSE: WebSocket endpoint for real-time updates
OWNER: Backend Team | RELATED: notification.py | LAST-AUDITED: 2026-01-31

WebSocket endpoint for real-time notifications and updates.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from jose import jwt, JWTError

from src.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/ws", tags=["WebSocket"])
settings = get_settings()


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}  # user_id -> websockets
        self.connection_count: int = 0
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self.connection_count += 1
        logger.info(f"WebSocket connected: user_id={user_id}, total={self.connection_count}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove a WebSocket connection."""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        self.connection_count = max(0, self.connection_count - 1)
        logger.info(f"WebSocket disconnected: user_id={user_id}, total={self.connection_count}")
    
    async def send_personal(self, user_id: int, message: dict):
        """Send message to a specific user."""
        if user_id in self.active_connections:
            disconnected = []
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    disconnected.append(ws)
            for ws in disconnected:
                self.disconnect(ws, user_id)
    
    async def broadcast(self, message: dict, exclude_users: Set[int] = None):
        """Broadcast message to all connected users."""
        exclude_users = exclude_users or set()
        for user_id, connections in list(self.active_connections.items()):
            if user_id not in exclude_users:
                await self.send_personal(user_id, message)
    
    def get_stats(self) -> dict:
        """Get connection statistics."""
        return {
            "total_connections": self.connection_count,
            "unique_users": len(self.active_connections),
            "timestamp": datetime.utcnow().isoformat()
        }


manager = ConnectionManager()


def verify_ws_token(token: str) -> Optional[int]:
    """Verify WebSocket JWT token and return user_id."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for real-time updates."""
    user_id = verify_ws_token(token)
    if user_id is None:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "")
            
            if msg_type == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat()})
            elif msg_type == "subscribe":
                channel = data.get("channel")
                await websocket.send_json({"type": "subscribed", "channel": channel})
            else:
                await websocket.send_json({"type": "ack", "received": msg_type})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)


@router.get("/stats")
async def get_ws_stats():
    """Get WebSocket connection statistics."""
    return manager.get_stats()


# Helper function for sending notifications from other modules
async def send_notification(user_id: int, title: str, message: str, 
                           notification_type: str = "info", data: dict = None):
    """Send a real-time notification to a user."""
    await manager.send_personal(user_id, {
        "type": "notification",
        "title": title,
        "message": message,
        "notification_type": notification_type,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    })


async def broadcast_notification(title: str, message: str, 
                                notification_type: str = "info", data: dict = None):
    """Broadcast notification to all connected users."""
    await manager.broadcast({
        "type": "notification",
        "title": title,
        "message": message,
        "notification_type": notification_type,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    })
