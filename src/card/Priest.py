# priest.py

from card import Card

class Priest(Card):
    def __init__(self):
        super().__init__(
            name="Priest",
            value=2,
            description="Look at another player's hand."
        )

    async def play(self, game, player, target_info):
        """
        Allows the player to see another player's hand.

        Args:
            game (Game): The current game instance.
            player (Player): The player who played the card.
            target_info (dict): Contains 'target_player_id'.
        """
        target_player_id = target_info.get('target_player_id')

        # Validate target player
        target_player = game.get_player(target_player_id)
        if not target_player or not target_player.is_active:
            await player.send_message({'type': 'error', 'message': 'Invalid target player.'})
            return

        # Check if target is protected
        if target_player.is_protected:
            await game.notify_players({
                'type': 'action',
                'message': f"{player.user.name} tried to look at {target_player.user.name}'s hand but they are protected."
            })
            return

        # Reveal target's hand to the player
        target_card = target_player.hand[0]
        await player.send_message({
            'type': 'private_info',
            'message': f"{target_player.user.name}'s card is {target_card.value}-{target_card.name}."
        })

        await game.notify_players({
            'type': 'action',
            'message': f"{player.user.name} looked at {target_player.user.name}'s hand."
        }, exclude_player_ids={player.user.user_id})
