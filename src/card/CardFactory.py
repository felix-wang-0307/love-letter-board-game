# card_factory.py
from card.Card import Card
from card.Guard import Guard
from card.Priest import Priest
from card.King import King
# ... import other card classes

CARD_CLASSES = {
    'Guard': Guard,
    'Priest': Priest,
    'King': King,
}

def create_card(card_name):
    card_class = CARD_CLASSES.get(card_name)
    if card_class:
        return card_class()
    else:
        _not_implemented_card = Card(card_name, 0, "Not implemented")
        _not_implemented_card.play = lambda game, player, target_info: None
        return _not_implemented_card
        raise ValueError(f"Unknown card name: {card_name}")
