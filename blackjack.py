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

class Play(object):

    deck = Deck()


c = Card('spades', 'king')
# print(c)

t = Deck()
print(t)