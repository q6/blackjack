from time import sleep

class Card(object):

    card_values = {
        'Ace': 11,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    }

    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 3 or King
        """
        self.suit = suit.capitalize()
        self.rank = rank
        self.points = self.card_values[rank]

    def __str__(self):
        return '  {} of {}'.format(self.rank, self.suit)


class Deck(object):

    suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        """
        Create a deck with all cards in it.
        """
        self.deck = []
        for suit in self.suits:
            for value in self.ranks:
                self.deck.append(Card(suit, value))

    def __str__(self):
        """
        :return: print out all cards that are in the deck
        """
        lst = []
        for card in self.deck:
            # lst.append(Card.__str__(card))
            lst.append(str(card))
        return '\n'.join(lst)

    def remove(self, index):
        try:  # user might want to remove card that isn't in deck
            self.deck.pop(index)
            return True
        except IndexError:
            return False

    def pick_random_card(self):
        """
        :return: a randomly selected Card object from deck.
        """
        from random import randrange
        card_index = randrange(0, len(self.deck))  # pick a random card
        card = self.deck[card_index]  # store random card
        self.deck.pop(card_index)  # remove that card from the deck
        return card

class Player(object):

    def __init__(self):
        self.hand = []  # a list of Card objects

    def add_card_to_hand(self, card):
        """
        Assume card is a valid card object not in hand
        """
        self.hand.append(card)
        return card

    def remove_card_from_hand(self, card):
        """
        Assume card is a valid card object in hand
        """
        self.hand.remove(card)

    def clear_hand(self):
        self.hand = []

    def print_hand(self):
        print('\nPlayers hand:')
        for card in self.hand:
            print(str(card))

    def ace_in_hand(self):  # deprecated
        for card in self.hand:
            if card.face == 'Ace':
                return True
        return False

    def how_many_aces_in_hand(self):
        total = 0
        for card in self.hand:
            if card.rank == 'Ace':
                total += 1
        return total

    def caclulate_hand_points(self):
        """
        calculate the points of the current hand
        :return: True if user can keep playing, False otherwise
        """
        # damn aces are making this harder
        total = sum(card.points for card in self.hand)  # check when ace is high

        if total > 21:  # user will loose if they do not have an ace up their sleeve ;)
            for ace in range(self.how_many_aces_in_hand()):  # if no aces range will be []
                total -= 10  # and aces is either 11 or 1. Subtract 10 to get their hand with a low ace
                if total < 21:  # If the new score is below 21 they can keep playing
                    break
        return total

    def play_turn(self, deck):
        """
        Assume that the hand is not larger than 21 points
        returns the points of the hand to compare and see who won
        """
        print('\nIt is now the PLAYERS turn to hit or stay.')
        self.print_hand()  # show the user their hand 1st
        while True:  # could be infinite loop
            sleep(1.5)  # ass a small delay, makes it easier to read
            user_choice = input('Player: Would you like to stay or hit? (s to stay h to hit)')
            if user_choice == 's':  # user chooses to stay
                print('Player stays.')
                break
            else:  # user wants to hit
                print('Player hits.')
                card = self.add_card_to_hand(deck.pick_random_card())
                print(str(card))
                # print(str(self.hand[:-1]))  # print out just the new card that was added
                points = self.caclulate_hand_points()
                if points > 21:  # check if the hit put them above 21
                    break  # above 21, we do not ask hem if they want to hit or stay anymore
        return self.caclulate_hand_points()

    def play_turn_2(self, deck, auto_hit=False):
        """
        Allows a user to play "a turn", either the dealer (AI) or player.
        "a turn" comes after seeing your two cards and ends once you are busted or you stay.
        :param deck: A deck object, a deck to chose a card from is the user wants to hit.
        :param auto_hit: Dealer uses auto hit, player does not. By default this is a Player's method
        :return: Points. The combined points of all the cards in the hand at the end of the turn.
        """
        # set up the print message to address the appropriate person
        if auto_hit:
            player = 'Dealer'
        else:
            player = 'Player'

        print('\nIt is now the {}\'s turn'.format(player))
        self.print_hand()
        while True:  # danger zone
            points = self.caclulate_hand_points()
            if points > 21:  # BUSTED!
                print('\n{} is BUSTED!\n'.format(player))
                break
            else:  # bot hits under 17 automatically, player can git as long as he is under 21 points
                if auto_hit and points < 17:  # dealer can hit if he's at less than 17 points  # AI DEALER
                    print('\nDealer Hits')
                    card = self.add_card_to_hand(deck.pick_random_card())
                    print(str(card))
                elif not auto_hit:  # player can hit even if he is at 20, (x) _ (x)  # PLAYER
                    user_choice = input('Player: Do you want to stay or hit? (s to stay, h to hit)')
                    if user_choice == 's':  # player stays
                        break
                    else:
                        print('\nPlayer hits.')
                        card = self.add_card_to_hand(deck.pick_random_card())
                        print(str(card))

        return self.caclulate_hand_points()  # return the points to be able to see who wins


class Dealer(Player):

    def print_hand(self):
        print('\nDealers hand:')
        # print('DEALER HIDES 1ST CARD')  # turn off during testing
        for card in self.hand[:]:  # set back to [1:] to hide 1st card
            print(str(card))

    def did_dealer_win(self):  # maybe I don't need this function
        return self.caclulate_hand_points() == 21

    def play_turn(self, deck):
        """
        Assume that the dealer has not got a winning hand at start
        returns the points of the hand to compare and see who won
        """
        print('\nIt is now the DEALERS turn to hit or stay.')
        self.print_hand()  # show the user the dealers hand
        while True:  # could be infinite loop
            sleep(1.5)  # ass a small delay, makes it easier to read
            points = self.caclulate_hand_points()
            if points > 21:  # dealer is above 21
                print('\nDealer is busted!')
                break
            elif points <= 17:  # lower or equal to 18, hit it!
                print('\nDealer Hits')
                card = self.add_card_to_hand(deck.pick_random_card())
                print(str(card))
                # self.add_card_to_hand(deck.pick_random_card())
                # print(str(self.hand[:-1]))  # print out just the new card that was added
            else:  # stay
                print('Dealer Stays')
                break
        return self.caclulate_hand_points()


class Play(object):

    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player()

        # reset hand so that the user can keep playing
        self.player.clear_hand()
        self.dealer.clear_hand()

        self.turn_counter = 0  # even is dealer, odd is player
        self.players = [self.dealer, self.player]  # used in the while loop


    def deal_card_to_player(self, player):
        """
        deals the player a random card
        :param player: A player object or dealer
        :return: the card given to the player
        """
        card = player.add_card_to_hand(self.deck.pick_random_card())
        return card

    def turn(self, player):  # WIP/ might not need/use
        """
        Method only used for player, not AI dealer
        1. show the user their hand
        2. ask if user wants to hit or stay
        3. if they hit calculate the value again
        :return: points in the hand
        """
        player.print_hand()
        hit_or_stay = input('Do you want to hit or stay? (enter (enter y to hit n to stay)')
        if hit_or_stay == 'y':
            player.add_card_to_hand(self.deck.pick_random_card())
        # calculate the score, no need to calculate before because one cannot lose in the 1st two cards
        return player.caclulate_hand_points()

    def play_one_game(self):

        # deal each player 2 cards
        self.deal_card_to_player(self.player)
        self.deal_card_to_player(self.dealer)
        self.deal_card_to_player(self.player)
        self.deal_card_to_player(self.dealer)

        # DEBUG
        # rig hand so dealer gets ace
        # self.dealer.clear_hand()
        # self.dealer.add_card_to_hand(Card('Spades', 'Ace'))
        # self.dealer.add_card_to_hand(Card('Diamonds', 'Ace'))

        # show the cards after they've been dealt
        self.player.print_hand()
        self.dealer.print_hand()

        # DEBUG
        # if dealer has 21 at start he wins
        # dd = (self.dealer.did_dealer_win())
        # print(dd)

        # dealer goes first
        # dealer_score = self.dealer.play_turn(self.deck)  # old method
        dealer_score = self.dealer.play_turn_2(self.deck, True)  # auto_hit to true because dealer is a bot
        # print(dealer_score)  # DEBUG
        if dealer_score <= 21:  # dealer is not out of the game
            # player goes second
            player_score = self.player.play_turn_2(self.deck)

        # both parties are done taking cards, let see who won  # Hit or stay phase is over
        if dealer_score > 21:  # dealer is over
            winner = 'Player'
        elif player_score > 21:  # player is over
            winner = 'Dealer'
        elif player_score == dealer_score:  # tie, dealer wins
            winner = 'Dealer'
        else:  # who is the winner?
            winner = max((player_score, 'Player'), (dealer_score, 'Dealer'))[1]

        print('\nThe winner is: ' + winner)

    def play(self):
        keep_playing = 'y'
        while keep_playing == 'y':
            self.play_one_game()
            keep_playing = input('Do you want to keep playing? (enter y for yes no for no)')


p = Play()
p.play()
