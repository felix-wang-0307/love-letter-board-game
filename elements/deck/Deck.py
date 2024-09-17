# deck.py
import random

class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def discard(self, card):
        self.discard_pile.append(card)

