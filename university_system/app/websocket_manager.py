"""
Tracks which students currently have a live WebSocket connection open,
so notifications can be pushed to them instantly in addition to being
persisted in the database for later retrieval. Kept as a small
singleton-style registry since there must only ever be one shared map
of connections across the whole app.
"""

from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_connections: Dict[str, WebSocket] = {}
        return cls._instance

    async def connect(self, student_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[student_id] = websocket

    def disconnect(self, student_id: str):
        self.active_connections.pop(student_id, None)

    async def send_notification(self, student_id: str, message: dict) -> bool:
        ws = self.active_connections.get(student_id)
        if ws is not None:
            await ws.send_json(message)
            return True
        return False
