from game.card import Suit, Value, Card
from game.deck import Deck
from game.player import Player

class Game:
    def __init__(self, player_names):
        """
        handles game setup
        """        
        #define key attributes & check players are valid
        self.player_names = player_names
        self.player_count = len(player_names)

        self._valid_players_check(player_names)

        self.game_in_progress = True
        self.declared = None

        #initialise and shuffle the deck, and create an empty bin to store discards
        self.deck = Deck()
        self.deck.shuffle()
        self.bin = []

        #initialise all the players into a nested list, then deal 6 cards to each
        self.players = [Player(pn) for pn in player_names]
        self._deal_initial_hands()


    def _valid_players_check(self, player_names):
        #check that a valid number of players was entered
        if self.player_count == 0:
            raise ValueError("Please enter at least 1 player name.")
        elif self.player_count > 8:
            raise ValueError("Please enter no more than 8 player names.")

        #check names are unique
        unique_names = list(set(self.player_names))
        if len(unique_names) != self.player_count:
            raise ValueError("Please enter unique names.")


    def _deal_initial_hands(self):
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

        #determine & announce scores & winners
        winners = self._determine_winners()  
        self._announce_scores(winners)
            

    def _determine_winners(self):
        self.final_scores = [int(player.score()) for player in self.players]
        self.winning_score = min(self.final_scores)
        winner_list = [str(player) for player in self.players if player.score() == self.winning_score]
        return winner_list


    def _announce_scores(self, winners):
        winner_count = len(winners)
        for i in range(self.player_count):
            print(f"{self.player_names[i]} had a score of {self.final_scores[i]}")

        if winner_count == 1:
            winner = winners[0]
            print(f"{winner} won with a score of {self.winning_score}")
        elif winner_count > 1:
            print(f"It's a {winner_count}-way tie between {", ".join(winners)}, with a score of {self.winning_score}")
            





    def play_turn(self, player, declare_or_draw):
        if declare_or_draw == "declare":
            self.declared = player
            self.game_in_progress = False
            return None

        elif declare_or_draw == "draw":
            self._check_deck_empty()

            drawn = self.deck.draw_card()
            print(f"You drew {drawn}.")
            swap_available = False

            while True:
                keep_or_discard = self.input_keep_discard()
                swap_index = self._after_drawing(keep_or_discard)
                if swap_index == -1:
                    if drawn.value in [11,12]:
                        swap_available = True
                    break

                elif 0 <= swap_index <= 5:
                    #case where player wishes to keep in exchange for one of their own
                    if self.check_position_filled(player, swap_index):
                        drawn, player.hand[swap_index] = player.hand[swap_index], drawn
                        break
                    else:
                        pass
                else:
                    raise ValueError("Swap index must be integer, -1 <= index <= 5")

            self.bin.append(drawn)
            if swap_available:
                self.offer_swap(player, drawn.value)
                #offer a swap based on drawn
                pass

        else:
            raise ValueError("You must either draw or declare.")


    def _check_deck_empty(self):
        if len(self.deck.cards) == 0:
            print("Deck is empty. Shuffling the bin into a new deck.")
            for i in range(len(self.bin)):
                self.deck.cards.append(self.bin.pop())
            self.deck.shuffle()
            

    def _after_drawing(self, keep_or_discard):
        if keep_or_discard == "keep":
            print("You must choose a card from your own hand to swap out.")
            swap_index = self.input_select_card() - 1
            return swap_index
        
        elif keep_or_discard == "discard":
            return -1
        else:
            raise ValueError("You must either keep or discard.")


    def offer_swap(self, player, value: int):
        if value == 11:
            rank = "Jack"
            swap_type = "a seen swap"
        elif value == 12:
            rank = "Queen"
            swap_type = "an unseen swap"
        else:
            raise ValueError("Cannot make a swap with value other than 11 or 12.")
        
        print(f"You discarded a {rank}, which means you can make {swap_type}.")
        use_or_ignore = self.input_use_ignore()

        if use_or_ignore == "use":
            own_card = None
            opp_card = None

            print("You must now choose a player to swap with.")
            victim = self.input_select_player(player)

            while own_card == None:
                print("You must choose a card from your own hand.")
                own_card_index = self.input_select_card() - 1
                own_card = player.hand[own_card_index]

            while opp_card == None:
                print("You must choose a card from your opponent's hand.")
                opp_card_index = self.input_select_card() - 1
                opp_card = victim.hand[opp_card_index]
                
            if rank == "Jack":
                #present both cards to player
                #ask if they want to continue with the stop
                #if yes - pass
                #if no - exit func
                pass

            player.hand[own_card_index] = opp_card
            victim.hand[opp_card_index] = own_card
            print("Swap successful!")

        elif use_or_ignore == "ignore":
            return None
        else:
            raise ValueError("You must either use or ignore the swap.")

    def discard_opportunity(self):
        if not self.game_in_progress:
            return "You can no longer discard as the game has finished"
        players_not_out = self.list_players_not_out()
        for player in players_not_out:
            self.individual_discard(player)


    def list_players_not_out(self):
        players_not_out = [p for p in self.players if  not p.is_out]
        return players_not_out


    def individual_discard(self, player: Player):
        print(f"{player.name}, you may now discard on {self.bin[-1]}")
        discard_or_skip = None
        while True:
            discard_or_skip = self.input_discard_skip()
            if discard_or_skip == "skip":
                break
            elif discard_or_skip == "discard":
                discard_index = self.input_select_card() - 1
                discard = player.hand[discard_index]

                if self.check_position_filled(player, discard_index):
                    if self.check_discard_valid(discard):
                        self.discard_from_hand(player, discard_index)
                        print("You may now discard again")

                    else:
                        print(f"You tried to discard illegally. You're out!")
                        player.is_out = True
                        break
                else:
                    print(f"No card found in position {discard_index + 1}")


    def check_discard_valid(self, discard):
        if len(self.bin) == 0:
            return False
        elif discard.value == self.bin[-1].value:
            return True
        else:
            return False

    def check_position_filled(self, player: Player, index: int):
        test = player.hand[index]
        if test == None:
            return False
        elif type(test) is Card:
            return True
        else:
            raise TypeError(f"Object of type {type(test)} found where expecting NoneType or Card.")
        

    def discard_from_hand(self, player, discard_index):
        discard = player.hand[discard_index]
        player.hand[discard_index] = None
        self.bin.append(discard)
        print(f"You successfully discarded {discard}")


    #runs the methods of the game in the correct logical order
    def run(self):
        while self.game_in_progress:
            for player in self.players:
                if self.game_in_progress:
                    if player.is_out:
                        pass
                    else:
                        draw_or_declare = self.input_draw_declare(player)
                        self.play_turn(player, draw_or_declare)
                        self.discard_opportunity()
                else:
                    self.end()




    ###***dedicated input methods follow:***###

    #declare or draw a card
    def input_draw_declare(self, player):
        print(f"{player.name}'s turn.")
        decision = input("Enter 'draw' to draw a card. Enter 'declare' to declare and end the game.")
        return decision

    #keep/discard a drawn card
    def input_keep_discard(self):
        decision = input("Enter 'keep' to keep this card. Enter 'discard' to discard it.")
        return decision

    #discard onto the bin or skip
    def input_discard_skip(self):
        decision = input("Enter 'discard' to discard a card. Enter 'skip' to skip.")
        return decision
    
    #use/ignore an 'action' card (Jack/Queen)
    def input_use_ignore(self):
        decision = input("Enter 'use' to use this card's action. Enter 'ignore' to ignore its action.")
        return decision

    #swap or retain own card (for seen swaps) THIS NEEDS CHANGING
    def input_swap_retain(self):
        decision = input("Enter 'swap' to swap your card with your opponent's. Enter 'retain' not to keep your card.")
        return decision

    #select a card from a hand
    def input_select_card(self):
        decision = int(input(f"Enter a card's position, 1-6, which you would like to select."))
        return decision

    #select a player to swap with
    def input_select_player(self, player):
        pn = input(f"Please select a player by entering a name from the following list: {", ".join([p.name for p in self.players if not p.is_out and p != player])}")
        index = self.player_names.index(pn)
        decision = self.players[index]
        return decision