import antigravity

class Card(object):

    card_values = {
        'ace': 11,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'jack': 10,
        'queen': 10,
        'king': 10
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

    suits = ['Spades', 'Diamonds', 'Heart', 'Clubs']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        """
        Create a deck with all cards in it.
        """
        self.deck = []
        for suit in self.suits:
            for value in self.values:
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

    def check_hand_value(self):
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
        for card in self.hand[1:]:
            print(str(card))


class Play(object):


    def __init__(self):
        self.deck = Deck()
        self.dealer = Player()
        self.player = Player()

        self.turn = 0  # even is dealer, odd is player

    def pick__random_card(self, deck):
        """
        :param deck: A Deck object
        :return: a randomly selected Card object from deck.
        """
        from random import randrange
        card_index = randrange(0, len(deck))  # pick a random card
        card = deck[card_index]  # store random card
        deck.remove(card_index)  # remove that card from the deck
        return card

    dealer_points = 0
    player_points = 0
    while player_points <= 21 or dealer_points <= 21:  # while nobody has over 21 points, keep playing
        



c = Card('spades', 'king')
# print(c)

t = Deck()
print(t)