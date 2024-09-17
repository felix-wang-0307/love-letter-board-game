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
        self.current_player_index = 0
        # TODO: Other initialization...
    
    def player_in_turn(self) -> Player:
        """
        Returns the player who is currently in turn.

        Returns:
            Player: The player in turn.
        """
        return self.players[self.current_player_index]

    def find_next_player(self, player: Player) -> Player:
        """
        Finds the next player in the list of players.

        Args:
            player (Player): The current player.

        Returns:
            Player: The next player.
        """
        index = self.players.index(player)
        next_index = (index + 1) % len(self.players)
        return self.players[next_index]

    def initialize_deck(self):
        """
        Initializes and shuffles the deck.
        """
        cards = []
        cards.extend([create_card("Guard") for _ in range(5)])
        cards.extend([create_card("Priest") for _ in range(2)])
        # TODO: add other cards based on game rules

        self.deck = Deck(cards)
        self.deck.shuffle()
    
    async def initialize(self, last_winners: Optional[List[Player]] = None):
        """Initializes the game."""
        # Initialize deck
        self.initialize_deck()
        # Initialize player states
        for player in self.players:
            player.__init__()
            await player.send_message({'type': 'game_start', 'message': 'The game has started!'})
        # Deal cards to players
        self.deal_cards()
        # Determine who plays first
        if last_winners:
            self.current_player_index = self.players.index(last_winners[0])
        else:
            self.current_player_index = 0

    async def deal_cards(self) -> None:
        """Starts the game."""
        for player in self.players:
            card = self.deck.draw()
            player.hand.append(card)
            await player.send_message(
                {
                    "type": "game_started",
                    "your_hand": [card.name for card in player.hand],
                }
            )

    async def handle_player_action(self, player_id, played_card_index, target_info):
        player = self.get_player(player_id)
        played_card = player.play_card(played_card_index)
        self.deck.discard(played_card)

        # Notify all players about the card played
        await self.notify_players(
            {
                "type": "card_played",
                "message": f"{player.user.name} played {played_card.name}.",
                "player_id": player_id,
                "card_name": played_card.name,
            }
        )

        # Execute the card's effect
        await played_card.play(self, player, target_info)

        # Proceed to the next turn
        await self.next_turn()

    async def notify_players(
        self, message: dict, exclude_player_ids: Optional[set] = None
    ):
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
    
    async def prepare_next_round(self, winners: List[Player]):
        """
        Prepares the game for the next round.
        """
        await self.initialize(winners)

    async def check_end_conditions(self):
        """
        Checks if the round has ended and handles the outcome.
        """
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) <= 1 or not self.deck.cards:
            # Round ends
            winners = self.determine_winner()
            await self.notify_players(
                {
                    "type": "round_end",
                    "message": "The round has ended.",
                    "winners": [p.user.name for p in winners],
                }
            )
            # Prepare for next round or end game
            await self.prepare_next_round(winners)

    async def determine_winner(self) -> List[Player]:
        """Logic to determine the winner"""
        active_players = [p for p in self.players if p.is_active]
        # Situation 1: Only 1 player left
        if len(active_players) == 1:
            return active_players
        # Situation 2: Multiple players left, compare hands
        # TODO: current version allows multiple winners, but later versions may have different rules, like checking the discard pile
        max_value = max([p.hand[0].value for p in active_players])
        winners = [p for p in active_players if p.hand[0].value == max_value]
        return winners