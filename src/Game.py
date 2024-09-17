# game.py
from server import manager
from deck import Deck
from player import Player

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = self.initialize_deck()
        self.current_player_index = 0
        self.is_active = True

    def initialize_deck(self):
        # Create all card instances and initialize the deck
        cards = [
            # Add the appropriate number of each card type
            # For example: 5 Guards, 2 Priests, etc.
        ]
        deck = Deck(cards)
        deck.shuffle()
        return deck

    def start(self):
        # Deal one card to each player
        for player in self.players:
            card = self.deck.draw()
            player.draw_card(card)
        self.next_turn()

    def next_turn(self):
        if not self.is_active:
            return

        current_player = self.players[self.current_player_index]
        if not current_player.is_active:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.next_turn()
            return

        # Draw a card
        drawn_card = self.deck.draw()
        current_player.draw_card(drawn_card)

        # Notify the player to make a move
        self.prompt_player_action(current_player)

    def prompt_player_action(self, player):
        # Send a message to the player's frontend to choose a card to play
        pass

    async def notify_players(self, message):
        for player in self.players:
            await manager.send_personal_message(message, player.player_id)

    async def handle_player_action(self, player_id, played_card_index, target_info):
        player = next(p for p in self.players if p.player_id == player_id)
        played_card = player.play_card(played_card_index)
        self.deck.discard(played_card)

        # Execute the card's effect
        await played_card.effect(self, player, **target_info)

        # Notify all players about the move
        await self.notify_players({
            'type': 'card_played',
            'player_id': player_id,
            'card': played_card.name,
            'target_info': target_info,
        })

        # Check for end-of-round conditions
        self.check_end_conditions()

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        await self.next_turn()


    def check_end_conditions(self):
        # Implement logic to check if the round or game has ended
        pass
