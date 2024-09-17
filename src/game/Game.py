# game.py
from typing import List, Optional
from player.Player import Player
from card.CardFactory import create_card
from deck.Deck import Deck

class Game:
    """
    Manages the Love Letter game logic.
    """

    def __init__(self, players: List[Player]):
        self.players = players
        # Other initialization...

    def initialize_deck(self):
        """
        Initializes and shuffles the deck.
        """
        cards = []
        cards.extend([create_card('Guard') for _ in range(5)])
        cards.extend([create_card('Priest') for _ in range(2)])
        # TODO: add other cards based on game rules

        self.deck = Deck(cards)
        self.deck.shuffle()

    async def start(self) -> None:
        """Starts the game."""
        # Game start logic...
        # Notify players
        for player in self.players:
            await player.send_message({
                'type': 'game_started',
                'your_hand': [card.name for card in player.hand]
            })
    
    async def handle_player_action(self, player_id, played_card_index, target_info):
        player = self.get_player(player_id)
        played_card = player.play_card(played_card_index)
        self.deck.discard(played_card)

        # Notify all players about the card played
        await self.notify_players({
            'type': 'card_played',
            'message': f"{player.user.name} played {played_card.name}.",
            'player_id': player_id,
            'card_name': played_card.name
        })

        # Execute the card's effect
        await played_card.play(self, player, target_info)

        # Proceed to the next turn
        await self.next_turn()
    
    async def notify_players(self, message: dict, exclude_player_ids: Optional[set] = None):
        """
        Sends a message to all players in the game.

        Args:
            message (dict): The message to send.
            exclude_player_ids (Optional[set]): Player IDs to exclude from receiving the message.
        """
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