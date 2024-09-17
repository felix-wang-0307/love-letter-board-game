from card.Card import Card
from player.Player import Player


class Baron(Card):
    def __init__(self):
        super().__init__(
            "Baron",
            3,
            "Compare hands with another player. The player with the lower value is eliminated from the round.",
        )

    async def play(self, game, player: Player, target_info):
        target_player_id = target_info.get("target_player_id")
        target_player = game.get_player(target_player_id)
        if not target_player or not target_player.is_active:
            player.send_message({"type": "error", "message": "Invalid target player."})
            return

        if target_player.is_protected:
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} tried to compare hands with {target_player.user.name} but they are protected.",
                }
            )
            return

        player_card_value = player.hand_value()
        target_card_value = target_player.hand_value()

        if player_card_value > target_card_value:
            target_player.is_active = False
            await game.notify_players(
                {
                    "type": "player_eliminated",
                    "message": f"{player.user.name} compared hands with {target_player.user.name} and won! {target_player.user.name} is eliminated.",
                    "player_id": target_player.user.user_id,
                }
            )
        elif player_card_value < target_card_value:
            player.is_active = False

            await game.notify_players(
                {
                    "type": "player_eliminated",
                    "message": f"{player.user.name} compared hands with {target_player.user.name} and lost! {player.user.name} is eliminated.",
                    "player_id": player.user.user_id,
                }
            )
        else:
            await game.notify_players(
                {
                    "type": "play_card",
                    "card": self.__repr__(),
                    "target": target_player.user.user_id,
                    "message": f"{player.user.name} compared hands with {target_player.user.name} and it's a tie!",
                }
            )
