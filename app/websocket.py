from fastapi import WebSocket
from typing import List

active_connections: List[WebSocket] = []

async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect(websocket: WebSocket):
    active_connections.remove(websocket)

async def notify_all(message: str):
    for connection in active_connections:
        await connection.send_text(message)
