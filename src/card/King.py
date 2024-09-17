from Card import Card

class King (Card):
    def __init__(self):
        super().__init__("King", 6, "Swap your hand with another's.")
    
    def on_play(self, player, target):
        player.hands, target.hands = target.hands, player.hands