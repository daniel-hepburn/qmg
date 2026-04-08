#each player object represents a hand of cards
#receive cards
#remove cards 

from game.card import Suit, Value, Card
from game.deck import Deck

class Player:
    def __init__(self,name):
        self.hand = []
        self.name = name

    def __str__(self):
        return f"{self.name}: {self.hand}" 
