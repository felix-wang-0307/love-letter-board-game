# user.py

from typing import Optional
from fastapi import WebSocket
import uuid

class User:
    """
    Represents a connected user.

    Attributes:
        user_id (str): Unique identifier for the user.
        name (Optional[str]): Display name of the user.
        websocket (WebSocket): The WebSocket connection associated with the user.
        current_room (Optional[GameRoom]): The game room the user is currently in.
    """

    def __init__(self, user_id: Optional[str], websocket: WebSocket, name: Optional[str] = None):
        self.user_id = user_id if user_id else str(uuid.uuid4())  # If user_id is None, generate a new UUID
        self.name = name or f"User {user_id}"
        self.websocket = websocket
        self.current_room = None  # Will be set when the user joins a room

    async def send_message(self, message: dict) -> None:
        """Sends a message to the user."""
        await self.websocket.send_json(message)

    async def disconnect(self) -> None:
        """Handles user disconnection."""
        await self.websocket.close()
        # Additional cleanup if necessary
