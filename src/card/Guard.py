# guard.py

from __future__ import annotations
from card.Card import Card
from player.Player import Player

class Guard(Card):
    def __init__(self):
        super().__init__(
            name="Guard",
            value=1,
            description="Guess another player's hand. If guessed correctly, the target player is eliminated."
        )

    async def play(self, game, player, target_info):
        """
        Allows the player to guess another player's hand. If guessed correctly, the target player is eliminated.

        Args:
            game (Game): The current game instance.
            player (Player): The player who played the card.
            target_info (dict): Contains 'target_player_id' and 'guessed_value'.
        """
        target_player_id = target_info.get('target_player_id')
        guessed_value = target_info.get('guessed_value')

        # Validate target player
        target_player: Player = game.get_player(target_player_id)
        if not target_player or not target_player.is_active:
            await player.send_message({'type': 'error', 'message': 'Invalid target player.'})
            return

        # Cannot guess Guard
        if guessed_value == 1:
            await player.send_message({'type': 'error', 'message': 'You cannot guess Guard.'})
            return

        # Check if target is protected
        if target_player.is_protected:
            await game.notify_players({
                'type': 'play_card',
                'target': target_player.user.user_id,
                'message': f"{player.user.name} tried to guess {target_player.user.name}'s card but they are protected."
            })
            return
        
        # Check if target's hand is assassin
        if target_player.hand[0].name == 'Assassin':
            player.is_active = False  # Eliminate the player who guessed
            await game.notify_players({
                'type': 'play_card',
                'target': target_player.user.user_id,
                'message': f"{player.user.name} tried to guess {target_player.user.name}'s card and be assassinated."
            })
            await game.check_end_conditions()
            return

        # Check if guess is correct
        target_card = target_player.hand[0]
        if target_card.value == guessed_value:
            # Eliminate the target player
            target_player.is_active = False
            await game.notify_players({
                'type': 'player_eliminated',
                'message': f"{player.user.name} guessed {target_player.user.name}'s card as {guessed_value} correctly! {target_player.user.name} is eliminated.",
                'player_id': target_player.user.user_id
            })
            # Check for end of round
            await game.check_end_conditions()
        else:
            await game.notify_players({
                'type': 'play_card',
                'target': target_player.user.user_id,
                'message': f"{player.user.name} guessed {target_player.user.name}'s card as {guessed_value}, but they guessed incorrectly."
            })
