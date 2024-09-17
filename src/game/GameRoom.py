# game_room.py

from typing import List, Optional
from user.User import User
from game.Game import Game
from player.Player import Player

class GameRoom:
    """
    Represents a game room where users can join to play.

    Attributes:
        room_id (str): Unique identifier for the game room.
        users (List[User]): List of users in the room.
        game_instance (Optional[Game]): The game instance if the game has started.
    """

    def __init__(self, room_id: str):
        self.room_id = room_id
        self.users: List[User] = []
        self.game_instance: Optional[Game] = None

    async def add_user(self, user: User) -> None:
        """Adds a user to the room."""
        self.users.append(user)
        user.current_room = self
        # Notify other users
        await self.broadcast({
            'type': 'user_joined',
            'user_id': user.user_id,
            'name': user.name
        }, exclude_user_ids={user.user_id})

    async def remove_user(self, user: User) -> None:
        """Removes a user from the room."""
        self.users.remove(user)
        user.current_room = None
        # Notify other users
        await self.broadcast({
            'type': 'user_left',
            'user_id': user.user_id
        })

        if not self.users:
            # Optionally, delete the room or handle cleanup
            pass

    async def broadcast(self, message: dict, exclude_user_ids: Optional[set] = None) -> None:
        """Sends a message to all users in the room."""
        if exclude_user_ids is None:
            exclude_user_ids = set()
        for user in self.users:
            if user.user_id not in exclude_user_ids:
                await user.send_message(message)

    async def start_game(self) -> None:
        """Starts a new game with the users in the room."""
        # Convert users to players
        players = [Player(user) for user in self.users]
        self.game_instance = Game(players)
        await self.game_instance.start()
