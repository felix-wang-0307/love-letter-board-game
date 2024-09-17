# deck.py
import random
from time import time
from card.CardFactory import create_card

random.seed(time())

class Deck:
    def __init__(self, cards=[]):
        self.cards = cards
        self.discard_pile = []
    
    def initialize_classic_deck(self):
        """Initializes a classic deck of 16 cards"""
        cards = []
        cards.extend([create_card("Guard") for _ in range(5)])
        cards.extend([create_card("Priest") for _ in range(2)])
        cards.extend([create_card("Baron") for _ in range(2)])
        cards.extend([create_card("Handmaid") for _ in range(2)])
        cards.extend([create_card("Prince") for _ in range(2)])
        cards.extend([create_card("King") for _ in range(1)])
        cards.extend([create_card("Countess") for _ in range(1)])
        cards.extend([create_card("Princess") for _ in range(1)])

        self.cards = cards
        self.shuffle()
    
    def initialize_extended_deck(self):
        """Initializes an extended deck of 32 cards"""
        cards = []
        # 0 value cards
        cards.extend([create_card("Assassin") for _ in range(1)])
        cards.extend([create_card("Jester") for _ in range(1)])
        # 1 value cards
        cards.extend([create_card("Guard") for _ in range(8)])
        # 2 value cards
        cards.extend([create_card("Priest") for _ in range(2)])
        cards.extend([create_card("Cardinal") for _ in range(2)])
        # 3 value cards
        cards.extend([create_card("Baron") for _ in range(2)])
        cards.extend([create_card("Baroness") for _ in range(2)])
        # 4 value cards
        cards.extend([create_card("Sycophant") for _ in range(2)])
        cards.extend([create_card("Handmaid") for _ in range(2)])
        # 5 value cards
        cards.extend([create_card("Prince") for _ in range(2)])
        cards.extend([create_card("Comet") for _ in range(2)])
        # 6 value cards
        cards.extend([create_card("King") for _ in range(1)])
        cards.extend([create_card("Constable") for _ in range(1)])
        # 7 value cards
        cards.extend([create_card("Countess") for _ in range(1)])
        cards.extend([create_card("Dowager Queen") for _ in range(1)])
        # 7.5 value cards
        cards.extend([create_card("Archbishop") for _ in range(1)])
        # 8 value cards
        cards.extend([create_card("Princess") for _ in range(1)])
        # 9 value cards
        cards.extend([create_card("Bishop") for _ in range(1)])

        self.cards = cards
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def discard(self, card):
        self.discard_pile.append(card)

    def is_empty(self):
        return not self.cards
