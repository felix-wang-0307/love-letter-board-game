from Card import Card
from player.Player import Player

class Princess (Card):
    def __init__(self):
        super().__init__("Princess", 8, "If the card is removed face-up from your hands, you will lose.")
    
    def on_play(self, player: Player, target):
        Player.alive = False