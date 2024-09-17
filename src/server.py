# server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from user.ConnectionManager import ConnectionManager
from user.User import User
from game.GameRoom import GameRoom
import uuid
from typing import Dict

app = FastAPI()
manager = ConnectionManager()
game_rooms: Dict[str, GameRoom] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for user connections.
    """
    user = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await handle_client_message(user, data)
    except WebSocketDisconnect:
        await manager.disconnect(user.user_id)
    except Exception as e:
        print(f"Error with user {user.user_id}: {e}")
        await manager.disconnect(user.user_id)

async def handle_client_message(user: User, data: dict):
    """
    Handles incoming messages from users.

    Args:
        user (User): The user who sent the message.
        data (dict): The message data.
    """
    message_type = data.get('type')
    if message_type == 'create_room':
        room_id = str(uuid.uuid4())[:8]
        game_room = GameRoom(room_id)
        game_rooms[room_id] = game_room
        await game_room.add_user(user)
        await user.send_message({
            'type': 'room_created',
            'room_id': room_id
        })
    elif message_type == 'join_room':
        room_id = data.get('room_id')
        game_room = game_rooms.get(room_id)
        if game_room:
            await game_room.add_user(user)
            await user.send_message({
                'type': 'room_joined',
                'room_id': room_id
            })
        else:
            await user.send_message({
                'type': 'error',
                'message': 'Room not found.'
            })
    elif message_type == 'leave_room':
        if user.current_room:
            await user.current_room.remove_user(user)
            await user.send_message({
                'type': 'room_left',
                'room_id': user.current_room.room_id
            })
    elif message_type == 'start_game':
        if user.current_room:
            await user.current_room.start_game()
    # Handle other message types...
