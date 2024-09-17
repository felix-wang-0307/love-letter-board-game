from card.Card import Card


class Countess(Card):
    def __init__(self):
        super().__init__(
            name="Countess",
            value=7,
            description="You must play this card if you have it and either the King or Prince in your hand. In all other cases, you can play this card.",
        )

    async def play(self, game, player, target_info):
        await game.notify_players(
            {
                "type": "play_card",
                "card": self.__repr__(),
                "target": player.user.user_id,
                "message": f"{player.user.name} played Countess. This card has no effects.",
            }
        )
