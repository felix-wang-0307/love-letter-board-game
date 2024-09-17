# card.py

class Card:
    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description

    def play(self, game, player, target_info):
        raise NotImplementedError("Each card must implement its play method.")

