#test code, ignore


from game.deck import Deck

if __name__ == "__main__":
    deck = Deck()
    print(len(deck))
    #deck.shuffle()
    print(deck.draw_card())
    print(len(deck))
    print(deck.cards)
    print(deck)