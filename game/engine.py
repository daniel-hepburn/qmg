from game.card import Suit, Value, Card
from game.deck import Deck
from game.player import Player

class Game:
    def __init__(self, player_names):
        """
        handles game setup
        """

        #check names are unique
        if player_names.sort() != list(set(player_names)).sort():
            raise ValueError("Please enter unqiue names")
        
        #define key attributes
        self.player_names = player_names
        self.player_count = len(player_names)
        self.game_in_progress = True
        self.declared = None

        #check that a valid number of players was entered
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

        #deal and print each player's hand
        print("Shuffling the deck & dealing 6 cards to each player:")
        for p in self.players:
            for i in range(6):
                p.hand.append(self.deck.draw_card())

            print(f"{p}'s hand: {p.hand}")


    #print player hands and scores, determine the winner, and end the game
    def end(self):
        #announce that the game is over & who declared
        print(f"Game over. {self.declared} declared.")

        #store scores in a list and calculate winners based on smallest final score
        final_scores = [int(player.score()) for player in self.players]
        min_score = min(final_scores)
        winners = [str(player) for player in self.players if player.score() == min_score]
        winner_count = len(winners)


        for i in range(self.player_count):
            print(f"{self.player_names[i]} had a score of {final_scores[i]}")
        
        if winner_count == 1:
            winner = winners[0]
            print(f"{winner} won with a score of {min_score}")

        elif winner_count > 1:
            print(f"It's a {winner_count}-way tie between {", ".join(winners)}, with a score of {min_score}")



    def player_card_swap(self, swapper, swap_type):
        victim_name = input("Please enter the name of the player with whom you would like to swap.")



    #current player can declare; otherwise they draw a card, and choose whether to swap it out for one of their own or discard it
    def play_turn(self, player):
        pn = self.player_names[self.players.index(player)]
        print(f"{pn}'s turn")
        declare_decision = input("Enter 'declare' to end the game now. Enter anything else to draw a card.")
        if declare_decision == "declare":
            self.declared = player 
            self.game_in_progress = False
        else:
            #check that the deck isn't empty; if it is, recycle & shuffle the bin
            if len(self.deck.cards) == 0:
                print("Deck is empty. Shuffling the bin into a new deck.")
                for i in range(len(self.bin)):
                    self.deck.cards.append(self.bin.pop())
                self.deck.shuffle()
                #code to shuffle bin into deck

            drawn = self.deck.draw_card()
            print(f"You drew {drawn}")
            
            #need to add try/except here
            decision = int(input(f"Enter a number 1-{len(player.hand)} to choose which of your cards to swap out, or enter 0 to discard without swapping."))
            if decision == 0:
                if drawn.value in [11,12]:
                    if drawn.value == 11:
                        swap_type = "seen"

                    elif drawn.value == 12:
                        swap_type = "blind"

                    swap_decision = input(f"You may now make a {swap_type} swap with another player. If you wish to continue, please enter the name of the player with whom you wish to swap. Enter anything else (i.e. not a player name) to skip.")
                    if swap_decision not in self.player_names:
                        pass
                    else:
                        victim = self.players[self.player_names.index(swap_decision)]
                        own_card = input(f"Enter a number, 1-{len(player.hand)}, to give away.")
                        victim_card = input(f"Enter a number, 1-{len(victim.hand)}, to take.")
#need to finish swap code from here-------------------------------------------------------------------------

                


            elif 1<= decision <= len(player.hand):
                drawn, player.hand[decision-1] = player.hand[decision-1], drawn
            else:
                raise ValueError("You must enter a number 0-6 to swap")
            
            self.bin.append(drawn)



    #ask all players if they want to discard on top of the bin
    def discard_opportunity(self):

        #check that the game is still active; if not it skips the rest of the method
        if not self.game_in_progress:
            print("Game over. You can no longer discard")
            return None
        else:
            pass
        
        #check that there is a card on the top of the bin for people to discard on
        #if so it prints that card so that people can see
        #if not it skips the rest of the method
        bin_size = len(self.bin)
        if bin_size == 0:
            print("No cards in the bin. You may not discard at this time.")
            return None
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
                print(f"{player}, you may now discard")

                #generating list of indices to remove from hand
                discard_indices = []
                card_count = len(player.hand)
                while -1 not in discard_indices:
                    try:
                        discard_choice = int(input(f"Top of bin: {self.bin[-1]}. \nSelect a card, 1-{card_count}, you would like to discard, or enter 0 to skip."))
                        if 0 <= discard_choice <= card_count:
                            discard_indices.append(discard_choice-1)                            
                        else:
                            print(f"You must enter a number between 1 and {card_count} (inclusive)")
                    except ValueError:
                        print("Please enter a number")
            
                for i in list(set(discard_indices)):
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
                else:
                    self.end()

#dedicated input methods follow:

#declare or draw a card
def input_declare_draw(self):
    decision = input("Enter 'draw' to draw a card. Enter 'declare' to declare and end the game.")
    return decision

#keep/discard a drawn card
def input_keep_discard(self):
    decision = input("Enter 'keep' to keep this card. Enter 'discard' to discard it.")
    return decision

#use/ignore an 'action' card (Jack/Queen)
def input_use_ignore(self):
    decision = input("Enter 'use' to go forward with this card's action. Enter 'ignore' to ignore its action.")
    return decision

#swap or retain own card (for seen swaps)
def input_swap_retain(self):
    decision = input("Enter 'swap' to swap with another player. Enter 'ignore' not to swap.")
    return decision

#select a card from a hand
def input_select_a_card(self):
    decision = input(f"Enter a card's position, 1-6, which you would like to select.")
    return decision


#select a player to swap with
def input_select_a_player(self):
    decision = input(f"Please select a player by entering a name from the following list: {", ".join(self.player_names)}")

