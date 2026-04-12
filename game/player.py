from game.card import Suit, Value, Card
from game.deck import Deck
import numpy as np

class Player:
    def __init__(self,name):
        self.hand = []
        self.name = name
        self.is_out = False

    def __str__(self):
        handstr = []
        for i in range(len(self.hand)):
            handstr.append(self.hand[i].__str__())
        return f"{self.name}'s hand:\n{self.hand}"
    
    def score(self):
        return np.sum([card.value for card in self.hand])
