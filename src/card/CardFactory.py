# card_factory.py

from Guard import Guard
from Priest import Priest
from King import King
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
        raise ValueError(f"Unknown card name: {card_name}")
