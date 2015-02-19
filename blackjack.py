def wait_for_user():
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

    def print_hand(self):
        print('\nPlayers hand:')
        for card in self.hand:
            print(str(card))

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
        wait_for_user()
        self.print_hand()
        while True:  # danger zone
            wait_for_user()  # add small delay
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
                    user_choice = input('\nPlayer: Do you want to stay or hit? (s to stay, h to hit)')
                    if user_choice == 's':  # player stays
                        print('\n{} stays.'.format(player))
                        break
                    else:  # player hits
                        print('\nPlayer hits.')
                        card = self.add_card_to_hand(deck.pick_random_card())
                        print(str(card))
                else:  # dealer stays  # AI DEALER
                    print('\n{} stays.'.format(player))
                    break

        return self.caclulate_hand_points()  # return the points to be able to see who wins


class Dealer(Player):

    def print_hand(self, hide_first_card=True):
        print('\nDealers hand:')
        if hide_first_card:
            print('  UNKNOWN')
        else:  # show 1st card
            print(str(self.hand[0]))
        for card in self.hand[1:]:  # set back to [1:] to hide 1st card
            print(str(card))

    def did_dealer_win(self):  # maybe I don't need this function
        return self.caclulate_hand_points() == 21


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
            # both parties are done taking cards, let see who won  # Hit or stay phase is over
            if dealer > 21:  # dealer is over
                winner = 'Player'
            elif player > 21:  # player is over
                winner = 'Dealer'
            elif player == dealer:  # tie, dealer wins
                winner = 'Dealer'
            else:  # who is the winner? highest cards wins
                winner = max((player, 'Player'), (dealer, 'Dealer'))[1]
            return winner

        # we check if the dealer has been dealt an instant winning hand
        # if not the dealer plays
        if self.dealer.did_dealer_win():  # instant win for dealer
            winner = 'Dealer'
        else:  # dealer did not instant win, DEALER plays
            dealer_score = self.dealer.play_turn(self.deck, True)  # auto_hit to true because dealer is a bot

        # after the dealer plays we check if he has 21, player looses and doesn't have to play
        if not self.dealer.did_dealer_win():  # dealer didn't win (get 21), player plays
            player_score = self.player.play_turn(self.deck)

            # both parties are done playing an we now compare cards to see who won.
            winner = get_winner_high_card(player_score, dealer_score)

        # Announce the winner
        wait_for_user()
        print('\n' + '=' * 20 + ' GAME FINISHED ' + '=' * 20)
        print('\nThe cards were:')
        self.player.print_hand()
        self.dealer.print_hand(False)
        wait_for_user()
        print('\nThe winner is: ' + winner)

    def play(self):
        keep_playing = 'y'
        while keep_playing == 'y':
            self.play_one_game()
            keep_playing = input('Do you want to keep playing? (enter y for yes no for no)')


p = Play()
p.play()
