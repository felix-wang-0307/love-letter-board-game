# player.py

from user.User import User
from card.Card import Card
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

    def reset(self):
        """
        Resets the player's state for a new round.
        """
        self.hand = []
        self.is_protected = False
        self.is_active = True
        self.has_played_constable = False
        self.jester_object = None
        self.comet_played = 0
        # Do not reset 'score' as it accumulates over rounds
    
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

    def play_card(self, card_index: int) -> Card:
        """
        Plays a card from the player's hand.

        Args:
            card_index (int): The index of the card in the player's hand.

        Returns:
            Card: The card that was played.

        Raises:
            ValueError: If the card index is invalid.
        """
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        else:
            raise ValueError("Invalid card index")
    
    def draw_card(self, card: Card) -> None:
        """
        Adds a card to the player's hand.

        Args:
            card (Card): The card to add to the player's hand.
        """
        self.hand.append(card)

    async def send_message(self, message: dict) -> None:
        """Sends a message to the player via their User instance."""
        await self.user.send_message(message)
    
    
