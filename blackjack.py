# static method test #2
def wait_for_user():  # should this really be global?
    input('\nPress enter to continue.\n')


class Card(object):

    card_values = {
        'Ace': 11,  # value of the ace is high until it needs to be low
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

    def __str__(self):  # deprecated (by ASCII print), but keep it in anyway
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
            lst.append(str(card))
        return '\n'.join(lst)

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

    def clear_hand(self):
        self.hand = []

    def print_hand(self, name='Player'):
        """
        Prints a nice ASCII version of the hand
        :param name: The when it prints it first says the name of who it's printing, check comments below
        """
        print('\n{} hand:'.format(name))  # at the end of the game dealer uses this method to print it's non-lipped over cards
        cards = []  # ASCII method needs to know all the cards that want to be printed before it can start printing them
        for card in self.hand:
            # print(str(card))  # deprecated by ASCII card print method
            cards.append(card)
        print(self.ascii_version_of_card(self.hand))

    @staticmethod
    def ascii_version_of_card(cards, start=0, return_string=True):
        """
        Instead of a boring text version of the card we render an ASCII image of the card.
        :param cards: One or more card objects
        :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
        keep it as a list so that the dealer can add a hidden card in front of the list
        """
        # we will use this to prints the appropriate icons for each card
        suits_name = 'Spades', 'Diamonds', 'Hearts', 'Clubs'
        suits_symbols = '♠', '♦', '♥', '♣'

        # create an empty list of list, each sublist is a line
        lines = [[] for i in range(9)]

        # print(self.hand)  # DEBUG
        # print(type(self.hand))  # DEBUG
        for index, card in enumerate(cards[start:]):
            # "King" should be "K" and "10" should still be "10"
            if card.rank == '10':  # ten is the only one who's rank is 2 char long
                rank = card.rank
                space = ''  # if we write "10" on the card that line will be 1 char to long
            else:
                rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
                space = ' '  # no "10", we use a blank space to will the void
            # get the cards suit in two steps
            suit = suits_name.index(card.suit)
            suit = suits_symbols[suit]

            # add the individual card on a line by line basis
            lines[0].append('┌─────────┐')
            lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
            lines[2].append('│         │')
            lines[3].append('│         │')
            lines[4].append('│    {}    │'.format(suit))
            lines[5].append('│         │')
            lines[6].append('│         │')
            lines[7].append('│       {}{}│'.format(space, rank))
            lines[8].append('└─────────┘')

        result = []
        for index, line in enumerate(lines):
            result.append(''.join(lines[index]))

        # hidden cards do not use string
        if return_string:
            return '\n'.join(result)
        else:
            return result

    def how_many_aces_in_hand(self):
        total = 0
        for card in self.hand:
            if card.rank == 'Ace':
                total += 1
        return total

    def calculate_hand_points(self):
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

    def play_turn(self, deck, auto_hit=False):
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

        wait_for_user()
        print('\nIt is now the {}\'s turn'.format(player))
        # wait_for_user()  # useless wait if v isn't activated anyway
        # self.print_hand()  # we do not need to show the hand after the user has just seen it
        while True:  # danger zone
            wait_for_user()  # add small delay
            points = self.calculate_hand_points()
            if points > 21:  # BUSTED!
                print('\n{} is BUSTED!\n'.format(player))
                break
            else:  # bot hits under 17 automatically, player can go as long as he is under 21 points
                if auto_hit and points < 17:  # dealer can hit if he's at less than 17 points  # AI DEALER
                    print('\nDealer Hits')
                    card = self.add_card_to_hand(deck.pick_random_card())
                    print(self.ascii_version_of_card([card]))
                elif not auto_hit:  # player can hit even if he is at 20, (x) _ (x)  # PLAYER
                    user_choice = input('\nPlayer: Do you want to stay or hit? (s to stay, h to hit)')
                    if user_choice == 's':  # player stays
                        print('\n{} stays.'.format(player))
                        break
                    else:  # player hits
                        print('\nPlayer hits.')
                        card = self.add_card_to_hand(deck.pick_random_card())
                        print(self.ascii_version_of_card([card]))
                else:  # dealer stays  # AI DEALER
                    print('\n{} stays.'.format(player))
                    break

        return self.calculate_hand_points()  # return the points to be able to see who wins


class Dealer(Player):

    def print_hand(self, hide_first_card=True):
        print('Dealers hand:')
        cards = []
        for card in self.hand:
            cards.append(card)
        print(self.ascii_version_of_hidden_card(self.hand))

    def ascii_version_of_hidden_card(self, cards):
        """
        Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
        :param cards: A list of card objects, the first will be hidden
        :return: A string, the nice ascii version of cards
        """
        # a flipper over card. # This is a list of lists instead of a list of string because appending to a list is better then adding a string
        lines = [
        ['┌─────────┐'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['│░░░░░░░░░│'],
        ['└─────────┘']
        ]


        # store the non-flipped over card after the one that is flipped over
        cards_except_first = self.ascii_version_of_card(self.hand, start=1, return_string=False)
        for index, line in enumerate(cards_except_first):
            lines[index].append(line)

        # make each line into a single list
        for index, line in enumerate(lines):
            lines[index] = ''.join(line)

        # convert the list into a single string
        return '\n'.join(lines)


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
        hit_or_stay = input('Do you want to hit or stay? (enter (enter y to hit n to stay)\n')
        if hit_or_stay == 'y':
            player.add_card_to_hand(self.deck.pick_random_card())
        # calculate the score, no need to calculate before because one cannot lose in the 1st two cards
        return player.calculate_hand_points()

    def play_one_game(self):

        # if the user wants to play multiple games we have to create a new deck and clear the hands
        self.deck = Deck()
        self.player.clear_hand()
        self.dealer.clear_hand()

        # deal each player 2 cards
        self.deal_card_to_player(self.player)
        self.deal_card_to_player(self.dealer)
        self.deal_card_to_player(self.player)
        self.deal_card_to_player(self.dealer)

        # show the users their cards
        self.player.print_hand()
        wait_for_user()
        self.dealer.print_hand()

        def get_winner_high_card(player, dealer):
            """
            both parties are done taking cards, let see who won  # Hit or stay phase is over
            :return: String, the name of winner we will announce in the next step ('Player' or 'Dealer")
            """
            # TODO instead of settings winner to string just return string
            if dealer > 21:  # dealer is over
                winner = 'Player'
            elif player > 21:  # player is over
                winner = 'Dealer'
            elif player == dealer:  # tie, dealer wins
                winner = 'Dealer'
            else:  # who is the winner? highest cards wins
                if player > dealer:  # player has higher card
                    winner = 'Player'
                else:  # dealer has the high card
                    winner = 'Dealer'
            return winner

        # we check if the dealer has been dealt an instant winning hand
        # if not the dealer actually plays
        def start_play_after_cards_dealt():
            """
            We put this code in it's own function because after we have a winner we do nto want to run another if or else
            :return: String, Who won the game.
            The function is invoked after the 2 cards have been dealt
            """
            if self.dealer.calculate_hand_points() == 21:  # instant win for dealer
                return 'Dealer'
            else:  # dealer did not instant win, DEALER plays
                dealer_score = self.dealer.play_turn(self.deck, True)  # auto_hit to true because dealer is a bot
            if dealer_score > 21:  # Dealer played and busted himself
                return 'Player'
            # after the dealer played check again if he has 21, if not the user can play
            if self.dealer.calculate_hand_points() == 21:
                return 'Dealer'
            else:  # After playing the dealer does not have a 21
                player_score = self.player.play_turn(self.deck)
            # after the dealer plays we check if he has 21, player automatically looses and doesn't have to play
            # if not self.dealer.calculate_hand_points() == 21:  # dealer didn't win (get 21), player plays
            #     player_score = self.player.play_turn(self.deck)

            # both parties are done playing an we now compare cards to see who won.
            return get_winner_high_card(player_score, dealer_score)  # we shouldn't have to call another functions ideally

        # after card have been dealt we can already start to see if there is a winner (only dealer can win at start though)
        winner = start_play_after_cards_dealt()

        # Announce the winner
        wait_for_user()
        print('\n' + '=' * 20 + ' GAME FINISHED ' + '=' * 20)
        print('The winner is: ' + winner)
        print('\nThe cards were:')
        self.player.print_hand()
        # self.dealer.print_hand(False)
        # noinspection PyCallByClass
        Player.print_hand(self.dealer, name='Dealer')

    def play(self):
        # Let the user know they are playing blackjack, do this only once
        print('='*20 + ' Welcome to Blackjack ' + '='*20)

        # allow the user to play many blackjack games
        keep_playing = 'y'
        while keep_playing == 'y':
            self.play_one_game()
            keep_playing = input('Do you want to keep playing? (enter y for yes no for no)\n')


p = Play()
p.play()
