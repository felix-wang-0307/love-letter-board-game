# game.py
from typing import List, Optional
from player.Player import Player
from deck.Deck import Deck

class Game:
    """
    Manages the Love Letter game logic.
    """

    def __init__(self, players: List[Player]):
        self.players = players
        self.current_player_index = 0
        self.deck: Deck = Deck()
        # TODO: Other initialization...
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """
        Retrieves a player by their user ID.

        Args:
            player_id (str): The user ID of the player.

        Returns:
            Optional[Player]: The player if found, else None.
        """
        for player in self.players:
            if player.user.user_id == player_id:
                return player
        return None

    async def next_turn(self):
        """
        Advances the game to the next player's turn, skipping inactive players.
        """
        await self.check_end_conditions()
        next_player = self.find_next_player(self.player_in_turn())
        if next_player.is_active:
            # It's the next player's turn
            await self.notify_players({
                "type": "next_turn",
                "player_id": next_player.user.user_id,
                "message": f"It's {next_player.user.name}'s turn."
            })
            # Draw a card if the deck is not empty
            if self.deck.cards:
                card = self.deck.draw()
                next_player.hand.append(card)
                await next_player.send_message({
                    "type": "draw_card",
                    "card_name": card.name
                })
            else:
                # No cards left to draw
                pass  # Handle end-of-deck situation if necessary
    
    def player_in_turn(self) -> Player:
        """
        Returns the player who is currently in turn.

        Returns:
            Player: The player in turn.
        """
        return self.players[self.current_player_index]

    def find_next_player(self, player: Player) -> Optional[Player]:
        """
        Finds the next active player in the list of players.

        Args:
            player (Player): The current player.

        Returns:
            Optional[Player]: The next active player, or None if no active players are left.
        """
        index = self.players.index(player)
        num_players = len(self.players)
        for _ in range(num_players):
            index = (index + 1) % num_players
            next_player = self.players[index]
            if next_player.is_active:
                return next_player
        return None  # No active players left


    def initialize_deck(self):
        """
        Initializes and shuffles the deck.
        """
        self.deck.initialize_classic_deck()
    
    async def initialize(self, last_winners: Optional[List[Player]] = None):
        """Initializes the game."""
        # Initialize deck
        self.initialize_deck()
        # Initialize player states
        for player in self.players:
            player.reset()
            await player.send_message({'type': 'game_start', 'message': 'The game has started!'})
        # Deal cards to players
        await self.deal_cards()
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
                    "type": "deal_card",
                    "your_hand": [card.name for card in player.hand],
                }
            )

    async def handle_player_action(self, player_id, played_card_index, target_info):
        """Handles a player's action in the game."""
        player = self.get_player(player_id)
        if not player:
            await player.send_message({'type': 'error', 'message': 'Player not found.'})
            return
        if player != self.player_in_turn():
            await player.send_message({'type': 'error', 'message': 'It is not your turn.'})
            return
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


# game.py

# ... [rest of your Game class code] ...

if __name__ == "__main__":
    import asyncio

    # Mock User class (since we're not considering connections)
    class MockUser:
        def __init__(self, user_id, name):
            self.user_id = user_id
            self.name = name

        async def send_message(self, message):
            print(f"Message to {self.name}: {message}")

    # Create mock users
    user1 = MockUser(user_id="1", name="Alice")
    user2 = MockUser(user_id="2", name="Bob")
    user3 = MockUser(user_id="3", name="Charlie")

    # Create players from mock users
    player1 = Player(user=user1)
    player2 = Player(user=user2)
    player3 = Player(user=user3)

    # Create a game with the players
    game = Game(players=[player1, player2, player3])

    # Since we're not running an async event loop in the usual way,
    # we'll define an async main function and run it with asyncio.

    async def main():
        # Initialize the game
        await game.initialize()

        # Simulate turns
        # For testing, we'll simulate each player's turn manually

        # Turn 1: Alice's turn
        current_player = game.player_in_turn()
        if current_player.user.name == "Alice":
            # Alice's hand should have one card from initialization
            # Simulate drawing a card
            if game.deck.cards:
                card_drawn = game.deck.draw()
                current_player.hand.append(card_drawn)
                await current_player.send_message({
                    "type": "draw_card",
                    "card_name": card_drawn.name
                })
            # Alice decides to play the first card in her hand
            await game.handle_player_action(
                player_id=current_player.user.user_id,
                played_card_index=0,
                target_info={'target_player_id': player2.user.user_id, 'guessed_card_name': 'Priest'}  # Example target info
            )

        # Turn 2: Bob's turn
        current_player = game.player_in_turn()
        if current_player.user.name == "Bob":
            # Simulate drawing a card
            if game.deck.cards:
                card_drawn = game.deck.draw()
                current_player.hand.append(card_drawn)
                await current_player.send_message({
                    "type": "draw_card",
                    "card_name": card_drawn.name
                })
            # Bob decides to play the first card in his hand
            await game.handle_player_action(
                player_id=current_player.user.user_id,
                played_card_index=0,
                target_info={'target_player_id': player3.user.user_id}
            )

        # Turn 3: Charlie's turn
        current_player = game.player_in_turn()
        if current_player.user.name == "Charlie":
            # Simulate drawing a card
            if game.deck.cards:
                card_drawn = game.deck.draw()
                current_player.hand.append(card_drawn)
                await current_player.send_message({
                    "type": "draw_card",
                    "card_name": card_drawn.name
                })
            # Charlie decides to play the first card in his hand
            await game.handle_player_action(
                player_id=current_player.user.user_id,
                played_card_index=0,
                target_info={'target_player_id': player1.user.user_id}
            )

        # Continue the simulation as needed
        # You can loop through the players and simulate actions until the game ends

    # Run the async main function
    asyncio.run(main())
