from card.Card import Card
from player.Player import Player


class Assassin(Card):
    def __init__(self):
        super().__init__(
            "Assassin",
            0,
            "If you are guessed by another player using a Guard, the player will be eliminated.",
        )

    async def play(self, game, player: Player, target_info):
        # playing the card does nothing
        await game.notify_players(
            {
                "type": "play_card",
                "card": self.__repr__(),
                "target": player.user.user_id,
                "message": f"{player.user.name} played Assassin. This card has no effects.",
            }
        )
