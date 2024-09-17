# player.py

from user import User

class Player:
    """
    Represents a player in the Love Letter game.

    Attributes:
        user (User): The associated User instance.
        hand (List[Card]): The player's hand.
        is_protected (bool): Whether the player is protected.
        is_active (bool): Whether the player is still active in the game.
    """

    def __init__(self, user: User):
        self.user = user
        self.hand = []
        self.is_protected = False
        self.is_active = True

    async def send_message(self, message: dict) -> None:
        """Sends a message to the player via their User instance."""
        await self.user.send_message(message)
