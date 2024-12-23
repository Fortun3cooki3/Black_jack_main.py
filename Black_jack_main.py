import random
import time

# making a deck of cards, first we need the cards them self
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11} #how to make ace 1 or 11


#this will give value to the cards and put them together
class Cards:
    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __radd__(self, other):  # makes the STR call work
        return self.value + other

    def __str__(self): # prints the cards in the player and dealer hands
        return f'{self.rank} of {self.suit}'

# creates a 52 card deck and shuffles them
class Deck:
    def __init__(self):
        self.full_deck = []
        for suit in suits:
            for rank in ranks:
                 self.full_deck.append(Cards(suit, rank))

    def shuffle (self): #shuffles the deck
         random.shuffle(self.full_deck)

    def dealer(self): #takes the top item away from the deck
        return self.full_deck.pop()

# class player hand, counting the total worth of points and a bank for money
class Player:
    def __init__(self, name):
        self.name = name
        self.new_cards = []
        self.card_counter = 0
        self.ace_counter = 0
        self.chips = 50

# adds card to players hand
    def add_card(self, new_card):
        self.new_cards.append(new_card)
        self.card_counter += values[new_card.rank]
        if new_card.rank == 'Ace':
            self.ace_counter += 1

    def ace_adjust(self):
        while self.card_counter > 21 and self.ace_counter:
            self.card_counter -= 10
            self.ace_counter -= 1

    def clear(self): #clears the player and dealer hand after every game
        self.new_cards.clear()

    # returns the card names of the player and the dealer
    def __str__(self):
        card = ", ".join(str(cardy) for cardy in self.new_cards)
        return card


#makes a bet, have to store it as a value, (bet)
    # player_one.chips, player_pc.chips = player_one.chips - a, player_pc.chips - a
def bets():
    the_bet = None
    while True:
        try:
            while the_bet not in list(range(1,21)):
                the_bet = int(input("amount to bet 1 to 20: "))

        except ValueError:
            print("sorry that is not a number")

        else:
            return the_bet

def restart():
    again = None

    while again not in ["y","n"]:
        again = input("play again? y/n ").lower()
        if again not in ['y','n']:
            print('sorry what?')
    if again == 'y':
        return True
    elif again == 'n':
        print("Game Over!")
        return False


#--------------------------------------------------------------------------------------------------------------------#

# game logic

#making while-loops
game_on = True # main game loop

print(input(
    f"\nWelcome to a little Black_jack game!\n\nthe goal of the game is to get as close to 21 as possible to win a hand. "
    f"and win all the chips from the bank!"
    f"\nbut be care full not to lose all your chips!\n\npress 'enter' to start the game!"))

while game_on: # starts the full game of black jack
    # start of the game. making players and introduction
    player_one = Player(input("whats you're name? ").capitalize())
    player_pc = Player('The dealer')

    black_jack = True  # hand loop
    black_jack_hand = True

    hit_stay = 'none'
    win = 'none'

    while black_jack: # every round of Black Jack


        #clear the players hands with the start of every round
        player_one.clear()
        player_pc.clear()
        player_one.card_counter = 0
        player_pc.card_counter = 0
        player_one.ace_counter = 0
        player_pc.ace_counter = 0


        # creating and shuffle the deck
        cards = Cards
        deck = Deck()
        deck.shuffle()
        print('') #prints a blank line
        print(f'{player_one.name} has {player_one.chips} chips!')
        print(f'{player_pc.name} has {player_pc.chips} chips!\n')

        #making a starting bet for player one.
        while True:
            bet = bets()
            if player_one.chips - bet < 0:
                print("not enough chips to bet!")
                continue
            elif player_pc.chips - bet < 0:
                print("The Dealer doesn't have enough chips to play!")
                continue
            else:
                break

        # pc player will always follow player_one bet
        player_one.chips, player_pc.chips = player_one.chips - bet, player_pc.chips - bet

        # creates the starting hand of both the player and the dealer
        player_one.add_card(deck.dealer())
        player_one.ace_adjust()
        player_one.add_card(deck.dealer())
        player_one.ace_adjust()
        player_pc.add_card(deck.dealer())
        player_pc.ace_adjust()
        player_pc.add_card(deck.dealer())
        player_pc.ace_adjust()

        print("")
        print(f'{player_one.name} has {player_one}')
        print(f'{player_one.card_counter} points\n')

        print(f'the {player_pc.name}: {player_pc.new_cards[0]} and one closed card\n')

        while black_jack_hand:
            # win check and hit/stay check
            hit_stay = 'none'
            win = 'none'

            # if the player wants to stay or get another card
            while hit_stay not in ['hit', 'stay']:
                win = 'none'
                hit_stay = (input('would you like to hit or stay? '))
                if hit_stay not in ['hit', 'stay']:
                    print('invalid choice')
                elif hit_stay in ['hit','stay']:
                    break

            if hit_stay == 'stay': # when player chooses the stay the Dealer starts to play
                print(" ")
                print(f'Dealer cards are {player_pc}')
                print(f'Dealer points are {player_pc.card_counter}')
                time.sleep(2)
                break

            elif hit_stay == 'hit': #when player hits for another card re-loops to card count
                print(" ")
                player_one.add_card(deck.dealer())
                player_one.ace_adjust()
                print(player_one)

                if player_one.card_counter > 21:
                    print(f'Bust with {player_one.card_counter} points')
                    win = 'bust'
                    break
                elif player_one.card_counter == 21:
                    print(f"You've got 21 Black Jack !\n")
                    win = 21
                    break
                elif player_one.card_counter < 21:
                    print(f'{player_one.card_counter}\n')


        if win == 'bust': #dealer gets the chips
            player_pc.chips = player_pc.chips + bet + bet


        elif win == 21: # if player_one has 21 points. Dealer still gets a chance to get 21.
            while player_pc.card_counter < player_one.card_counter:
                player_pc.add_card(deck.dealer())
                player_pc.ace_adjust()
                print(player_pc)
                print(player_pc.card_counter)
                time.sleep(2)

                if player_pc.card_counter > 21:
                    print(f'Dealer bust!\n{player_one.name} wins {bet} chips')
                    player_one.chips = player_one.chips + bet + bet
                    time.sleep(2)
                    break
                elif player_pc.card_counter == 21:
                    print(f'Dealer got 21 and wins {bet}')
                    player_pc.chips = player_pc.chips + bet + bet
                    time.sleep(2)
                    break

        elif hit_stay == 'stay': # the dealers turn
            while player_pc.card_counter:

                if  player_pc.card_counter < player_one.card_counter:
                    print(" ")
                    player_pc.add_card(deck.dealer())
                    player_pc.ace_adjust()
                    print(f"{player_pc}\n{player_pc.card_counter}")
                    time.sleep(2)

                elif player_pc.card_counter > 21:
                    print(f'Dealer bust!\n{player_one.name} wins {bet} chips')
                    player_one.chips = player_one.chips + bet + bet
                    time.sleep(2)
                    break

                elif player_pc.card_counter == 21:
                    print(f'Dealer got 21 and wins {bet}')
                    player_pc.chips = player_pc.chips + bet + bet
                    time.sleep(2)
                    break

                elif player_pc.card_counter == player_one.card_counter and player_pc.card_counter < 18:
                    continue

                elif player_pc.card_counter == player_one.card_counter and player_pc.card_counter >= 18:
                    print("It's a draw")
                    player_one.chips = player_one.chips + bet
                    player_pc.chips = player_pc.chips + bet
                    break

                elif player_pc.card_counter > player_one.card_counter:
                    print("The Dealer got higher and won")
                    player_pc.chips = player_pc.chips + bet + bet
                    break

        if player_one.chips == 0:
            print(" ")
            print("The Dealer has won the game! \nLoser...")
            black_jack = False
            black_jack_hand = False
            if restart():
                continue
            else:
                game_on = False

        if player_pc.chips == 0:
            print(" ")
            print(f"{player_one.name} Won the game!")
            black_jack = False
            black_jack_hand = False
            if restart():
                continue
            else:
                game_on = False





