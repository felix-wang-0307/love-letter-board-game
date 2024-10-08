from card.Card import Card
from player.Player import Player


class Prince(Card):
    def __init__(self):
        super().__init__(
            "Prince",
            5,
            "Choose any player (including yourself) to discard their hand and draw a new card from the deck.",
        )

    async def play(self, game, player: Player, target_info):
        target_player_id = target_info.get("target_player_id")
        target_player: Player = game.get_player(target_player_id)
        if not target_player or not target_player.is_active:
            await player.send_message(
                {"type": "error", "message": "Invalid target player."}
            )
            return

        if target_player.is_protected:
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} tried to make {target_player.user.name} discard their hand but they are protected.",
                }
            )
            return

        if game.deck.is_empty():
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} tried to make {target_player.user.name} discard their hand but the deck is empty.",
                }
            )
            return

        if target_player.hand[0].name == "Princess":
            target_player.is_active = False
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} made {target_player.user.name} discard their hand and draw a new card.",
                }
            )
            await game.notify_players(
                {
                    "type": "player_eliminated",
                    "message": f"{player.user.name} made {target_player.user.name} discard their Princess and thus they lost.",
                    "player_id": target_player.user.user_id,
                }
            )
            return

        discarded_card = target_player.hand.pop()
        card = game.deck.draw()
        target_player.draw_card(card)

        await game.notify_players(
            {
                "type": "play_card",
                "card": self.__repr__(),
                "target": target_player.user.user_id,
                "message": f"{player.user.name} made {target_player.user.name} discard their {discarded_card.__repr__()} and draw a new card.",
            }
        )

        await target_player.send_message(
            {
                "type": "private_info",
                "message": f"You discarded your {discarded_card.__repr__()} and drew a {card.__repr__()}.",
            }
        )
