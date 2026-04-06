from enum import Enum, IntEnum

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

class Value(IntEnum):
    ACE = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 1

class Card:
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value.name} of {self.suit.value}"

    __repr__ = __str__

if __name__ == "__main__":
    card = Card(Suit.HEARTS, Value.ACE)
    print(card)

