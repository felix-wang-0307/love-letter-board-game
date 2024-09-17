from card.Card import Card
from player.Player import Player

class Princess (Card):
    def __init__(self):
        super().__init__("Princess", 8, "If the card is removed face-up from your hands, you will lose.")

    async def play(self, game, player: Player, target_info):
        player.is_active = False
        await game.notify_players({
            'type': 'player_eliminated',
            'message': f"{player.user.name} discarded their Princess and thus they lost.",
            'player_id': player.user.user_id
        })