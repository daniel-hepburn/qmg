from game.card import Suit, Value, Card
from game.deck import Deck
from game.player import Player

class Game:
    def __init__(self, player_names):
        self.player_names = player_names
        self.game_in_progress = True
        self.player_count = len(player_names)
        self.declared = None

        #checking that a valid number of players was entered
        if self.player_count == 0:
            raise ValueError("Please enter at least 1 player name")
        elif self.player_count > 8:
            raise ValueError("Please enter no more than 8 player names")
        
        #initialise and shuffle the deck
        self.deck = Deck()
        self.deck.shuffle()

        #create a bin to store discards
        self.bin = []

        #initialise all the players into a nested list
        self.players = [Player(pn) for pn in player_names]

        #dealing 6 cards to each player 
        for p in self.players:
            for i in range(6):
                p.hand.append(self.deck.draw_card())

            print(p)


    #print player hands and scores, determine the winner, and end the game
    def end(self):

        final_scores = [int(player.score()) for player in self.players]
        min_score = min(final_scores)
        winners = [player for player in self.players if player.score() == min_score]

        #start test
        to_return = []
        for i in range(self.player_count):
            to_return.append(f"{self.player_names[i]} had a score of {final_scores[i]}")
        
        to_return.append(f"Game over. {self.declared} declared.\nWinner(s): {winners} with a score of {min_score}")
        
        return to_return
        #end test (original code is 3 lines commented out below)

        #for i in range(self.player_count):
        #    print(f"{self.player_names[i]} had a score of {final_scores[i]}")
        
        #return f"Game over. {self.declared} declared.\nWinner(s): {winners} with a score of {min_score}"


    #current player can declare; otherwise they draw a card, and choose whether to swap it out for one of their own or discard it
    def play_turn(self, player):
        pn = self.player_names[self.players.index(player)]
        print(f"{pn}'s turn")
        declare_decision = input("Type declare to end the game now. Enter anything else to draw a card.")
        if declare_decision == "declare":
            self.declared = player 
            self.game_in_progress = False
        else:
            drawn = self.deck.draw_card()
            print(f"You drew {drawn}")
            swap = int(input("Enter a number 1-6 to choose which of your cards to swap out, or enter 0 to discard without swapping."))
            if swap == 0:
                pass
            elif swap > 0 and swap < 7:
                drawn, player.hand[swap-1] = player.hand[swap-1], drawn
            else:
                raise ValueError("You must enter a number 0-6 to swap")
            
            self.bin.append(drawn)



    #ask all players if they want to discard on top of the bin
    def discard_opportunity(self):

        #check that the game is still active; if not it skips the rest of the method
        if self.game_in_progress:
            pass
        else:
            return None
        
        #check that there is a card on the top of the bin for people to discard on
        #if so it prints that card so that people can see
        #if not it skips the rest of the method
        bin_size = len(self.bin)
        if bin_size == 0:
            return "No cards in the bin. You may not discard at this time."
        else:
            print(f"Top card: {self.bin[-1]}")

        #loops through the players asking if they want to discard
        #for each player, it asks for the position of a card they want to discard 
        #moves to next player once they enter 0
        #note - this removes the cards' positions altogether rather than leaving an empty string

        for player in self.players:
            #check if the player has crashed out, or if they have no cards to discard
            if player.is_out:
                print(f"{player.name} is out and cannot discard.")
            elif len(player.hand) == 0:
                print(f"{player.name} has no cards and cannot discard.")
            else:
                print(f"{player} You may now discard")

                #generating list of indices to remove from hand
                discard_indices = []
                card_count = len(player.hand)
                while -1 not in discard_indices:
                    try:
                        discard_choice = int(input(f"Top of bin: {self.bin[-1]}. \nSelect a card, 1-{card_count}, you would like to discard, or enter 0 to skip."))
                        if 0 <= discard_choice <= card_count:
                            discard_indices.append(discard_choice-1)
                            break
                        else:
                            print(f"You must enter a number between 1 and {card_count} (inclusive)")
                    except ValueError:
                        print("Please enter a number")
            
                for i in discard_indices:
                    if i >= 0:
                        if player.hand[i].value == self.bin[-1].value:
                            self.bin.append(player.hand.pop(i))
                        else:
                            print(f"You tried to discard {player.hand[i]} on top of {self.bin[-1]}. You're out!")
                            player.is_out = True
                            break
                        print("Discarded successfully.")
                    else:
                        break        


    #runs the methods of the game in the correct logical order
    def run(self):
        while self.game_in_progress:
            for player in self.players:
                if self.game_in_progress:
                    if player.is_out:
                        pass
                    else:
                        self.play_turn(player)
                        self.discard_opportunity()

        self.end()