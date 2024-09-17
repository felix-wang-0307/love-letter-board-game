# card.py
class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def play(self, game, player, target_info):
        raise NotImplementedError("Each card must implement its play method.")

# Use reflection to create card instances
def create_card_from_name(card_name):
    module = __import__('card')
    card_class = getattr(module, card_name)
    return card_class()