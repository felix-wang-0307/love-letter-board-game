# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # player_id: WebSocket

    async def connect(self, websocket: WebSocket, player_id: str):
        await websocket.accept()
        self.active_connections[player_id] = websocket

    def disconnect(self, player_id: str):
        del self.active_connections[player_id]

    async def send_personal_message(self, message: dict, player_id: str):
        websocket = self.active_connections[player_id]
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(websocket, player_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Handle incoming messages from clients
            await handle_client_message(player_id, data)
    except WebSocketDisconnect:
        manager.disconnect(player_id)

async def handle_client_message(player_id: str, data: dict):
    # Process the message based on the game logic
    pass
