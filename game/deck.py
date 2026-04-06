from game.card import Suit, Value, Card
import random

class Deck:

    def __init__(self):
        self.cards = [Card(suit,value) for suit in Suit for value in Value]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Deck of {len(self)} cards"
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()



if __name__ == "__main__":
    deck = Deck()
    print(len(deck))
    deck.shuffle()
    print(deck.draw_card())
    print(len(deck))
    