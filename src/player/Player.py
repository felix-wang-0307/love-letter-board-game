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
        has_played_constable (bool): Whether the player has played Constable.
        jester_object (Player): The player who played Jester on this player.
        comet_played (int): Number of times the player has played a Comet.
        score (int): The player's score.
    """

    def __init__(self, user: User):
        self.user = user
        self.hand = []
        self.is_protected = False  # protected by Handmaid
        self.is_active = True  # eliminated if false, alive if true
        self.has_played_constable = False  # used to track if Constable has been played
        self.jester_object: Player = None  # Who played the Jester on this player
        self.comet_played: int = 0  # Number of times the player has played a comet 
        self.score: int = 0
    
    def hand_value(self) -> int:
        """Returns the value of the player's hand."""
        return self.hand[0].value
    
    def final_hand_value(self) -> int:
        """Returns the value of the player's hand when determining the winner."""
        return self.hand_value() + self.comet_played
    
    def win_turn(self):
        """Handles score changes when the player wins a turn."""
        self.score += 1
        if self.jester_object:
            self.jester_object.score += 1
    
    def lose_turn(self):
        """Handles score changes when the player loses a turn."""
        if self.has_played_constable:
            self.score += 1

    async def send_message(self, message: dict) -> None:
        """Sends a message to the player via their User instance."""
        await self.user.send_message(message)
