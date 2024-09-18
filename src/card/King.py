# priest.py

from card.Card import Card
from player.Player import Player
from typing import Dict, Optional


class King(Card):
    def __init__(self):
        super().__init__(
            name="King",
            value=6,
            description="Swap hands with another player of your choice.",
        )

    async def play(self, game, player: Player, target_info: Dict[str, str]) -> None:
        """
        Allows the player to swap hands with another player of their choice.

        Args:
            game (Game): The current game instance.
            player (Player): The player who played the card.
            target_info (dict): Contains 'target_player_id'.
        """
        target_player_id = target_info.get("target_player_id")

        # Validate target player
        target_player = game.get_player(target_player_id)
        if not target_player or not target_player.is_active:
            await player.send_message(
                {"type": "error", "message": "Invalid target player."}
            )
            return

        # Check if target is protected
        if target_player.is_protected:
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} tried to swap hands with {target_player.user.name} but they are protected.",
                }
            )
            return

        # Swap hands
        player.hand, target_player.hand = target_player.hand, player.hand

        await game.notify_players(
            {
                "type": "play_card",
                "card": self.__repr__(),
                "target": target_player.user.user_id,
                "message": f"{player.user.name} swapped hands with {target_player.user.name}.",
            }
        )

        await player.send_message(
            {
                "type": "private_info",
                "message": f"You swapped hands with {target_player.user.name} and got a {player.hand}.",
            }
        )

        await target_player.send_message(
            {
                "type": "private_info",
                "message": f"You swapped hands with {player.user.name} and got a {target_player.hand}.",
            }
        )
        
