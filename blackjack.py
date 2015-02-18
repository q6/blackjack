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
        return '{} of {}'.format(self.rank, self.suit)


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
        self.hand = []

    def add_card_to_hand(self, card):
        """
        Assume card is a valid card object not in hand
        """
        self.hand.append(card)

    def remove_card_from_hand(self, card):
        """
        Assume card is a valid card object in hand
        """
        self.hand.remove(card)

    def clear_hand(self):
        self.hand = []

    def print_hand(self):
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
            if card.face == 'Ace':
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




class Dealer(Player):

    def print_hand(self):
        print('DEALER HIDES 1ST CARD')
        for card in self.hand[:]:  # set back to [1:] to hide 1st card
            print(str(card))


class Play(object):


    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player()

        self.players = [self.dealer, self.player]  # used in the while loop



    def deal_card_to_player(self, player):
        """
        deals the player a random card
        :param player: A player object or dealer
        :return: the card given to the player
        """
        card = player.add_card_to_hand(self.deck.pick_random_card())
        return card


    def turn(self, player):
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

    def play(self):
        dealer_points = 0
        player_points = 0
        dealer_keeps_playing = True
        player_keeps_playing = True
        turn_counter = 0  # even is dealer, odd is player

        # for now kinda hard coded the moves AIDS
        # first deal each player two cards, then show the two card. p -> d -> p -> d
        self.deal_card_to_player(self.player)  # this function call seems weird, ?player.deal_card_to_player()? better?
        self.deal_card_to_player(self.dealer)
        self.deal_card_to_player(self.player)
        self.deal_card_to_player(self.dealer)
        self.player.print_hand()
        print()  # ^ player, v dealer
        self.dealer.print_hand()

        while dealer_keeps_playing or player_keeps_playing:  # while nobody has over 21 points, keep playing
            if turn_counter % 2 == 0:  # is even, dealers turn
                print('Dealer\'s Turn')
                dealer_points = self.dealer.caclulate_hand_points()
                if dealer_points > 21:  # dealer is over 21 -> lose
                    print('Dealer Loses')
                    dealer_keeps_playing = False
                elif dealer_points <= 17:  # dealer points is 17 or lower, hit it!
                    self.dealer.add_card_to_hand(self.deck.pick_random_card())
                else:  # dealer is between 17 and 21, we stay!
                    dealer_keeps_playing = False
                turn_counter += 1
            else:  # it's the players turn
                print('Player\'s Turn')
                player_points = self.turn(self.player)
                if player_points > 21:
                    print('Player Looses')
                    player_keeps_playing = False
                else:  # redundant
                    player_keeps_playing = True
                turn_counter += 1


p = Play()
p.play()
