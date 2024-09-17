from card.Card import Card
from player.Player import Player


class Handmaid(Card):
    def __init__(self):
        super().__init__(
            "Handmaid",
            4,
            "Until your next turn, ignore all effects from other players' cards.",
        )

    async def play(self, game, player: Player, target_info):
        player.is_protected = True
        await game.notify_players(
            {
                "type": "play_card",
                "card": self.__repr__(),
                "target": player.user.user_id,  # target is the player who played the card
                "message": f"{player.user.name} played Handmaid and is protected until their next turn.",
            }
        )
