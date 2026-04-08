#test code, ignore


from game.deck import Deck
from game.player import Player

if __name__ == "__main__":
    player1 = Player("dan"); player2 = Player("dad")
    deck = Deck(); deck.shuffle()
    for i in range(6):
        player1.hand.append(deck.draw_card()); player2.hand.append(deck.draw_card())
        print(f"Draw {i+1} -- Player 1: {player1.hand}. Player 2: {player2.hand}")

