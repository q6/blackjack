class Card(object):

    def __init__(self, suit, value):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param value: The value of the card, e.g 3 or King
        """
        self.suit = suit.capitalize()
        self.value = value

    def __str__(self):
        return '{} of {}'.format(self.value, self.suit)


class Deck(object):

    suits = ['Spades', 'Diamonds', 'Heart', 'Clubs']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

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

    




c = Card('spades', 'king')
# print(c)

t = Deck()
print(t)