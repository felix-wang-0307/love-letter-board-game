# game.py
from typing import List, Optional
from player.Player import Player

class Game:
    """
    Manages the Love Letter game logic.
    """

    def __init__(self, players: List[Player]):
        self.players = players
        # Other initialization...

    async def start(self) -> None:
        """Starts the game."""
        # Game start logic...
        # Notify players
        for player in self.players:
            await player.send_message({
                'type': 'game_started',
                'your_hand': [card.name for card in player.hand]
            })

    async def notify_players(self, message: dict, exclude_player_ids: Optional[set] = None) -> None:
        """Sends a message to all players in the game."""
        if exclude_player_ids is None:
            exclude_player_ids = set()
        for player in self.players:
            if player.user.user_id not in exclude_player_ids:
                await player.send_message(message)

    async def check_end_conditions(self):
        """
        Checks if the round has ended and handles the outcome.
        """
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) <= 1 or not self.deck.cards:
            # Round ends
            winner = self.determine_winner()
            await self.notify_players({
                'type': 'round_end',
                'message': f"The round has ended. {winner.user.name} wins the round!",
                'winner_id': winner.user.user_id
            })
            # Prepare for next round or end game
            await self.prepare_next_round()