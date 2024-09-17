from Card import Card
from player.Player import Player

class Princess (Card):
    def __init__(self):
        super().__init__("Princess", 8, "If the card is removed face-up from your hands, you will lose.")

    def play(self, game, player, target_info):
        raise NotImplementedError("Each card must implement its play method.")