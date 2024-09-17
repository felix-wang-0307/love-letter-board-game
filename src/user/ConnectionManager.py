# connection_manager.py

from typing import Dict, Optional
from fastapi import WebSocket
from user.User import User
import uuid

class ConnectionManager:
    """
    Manages User connections for the Love Letter game.
    """

    def __init__(self):
        self.active_users: Dict[str, User] = {}

    async def connect(self, websocket: WebSocket) -> User:
        """
        Accepts a WebSocket connection and creates a new User.

        Args:
            websocket (WebSocket): The WebSocket connection to the client.

        Returns:
            User: The created User instance.
        """
        await websocket.accept()
        user_id = str(uuid.uuid4())
        user = User(user_id=user_id, websocket=websocket)
        self.active_users[user_id] = user
        print(f"User {user_id} connected.")
        return user

    # connection_manager.py (updated disconnect method)

    async def disconnect(self, user_id: str) -> None:
        """
        Removes a User from active connections and handles cleanup.

        Args:
            user_id (str): The unique identifier of the user.
        """
        user = self.active_users.pop(user_id, None)
        if user:
            if user.current_room:
                await user.current_room.remove_user(user)
            await user.disconnect()
            print(f"User {user_id} disconnected.")


    async def send_personal_message(self, message: dict, user_id: str) -> None:
        """
        Sends a message to a specific user.

        Args:
            message (dict): The message to send.
            user_id (str): The unique identifier of the user.
        """
        user = self.active_users.get(user_id)
        if user:
            await user.send_message(message)
        else:
            print(f"Cannot send message to user {user_id}: User not found.")

    async def broadcast(self, message: dict, exclude_user_ids: Optional[set] = None) -> None:
        """
        Broadcasts a message to all connected users, optionally excluding some.

        Args:
            message (dict): The message to broadcast.
            exclude_user_ids (Optional[set]): A set of user IDs to exclude.
        """
        if exclude_user_ids is None:
            exclude_user_ids = set()
        for user_id, user in self.active_users.items():
            if user_id not in exclude_user_ids:
                await user.send_message(message)
