from blackjack import Card

def convert_card_to_ascii(*cards):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create the empty list to add card parts to
    line_1 = []
    line_2 = []
    line_3 = []
    line_4 = []
    line_5 = []
    line_6 = []
    line_7 = []
    line_8 = []
    line_9 = []

    for card in cards:
        rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
        # get the cards suit in two steps
        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        # add the individual card on a line by line basis
        line_1.append('┌─────────┐')
        line_2.append('│{}        │'.format(rank))
        line_3.append('│         │')
        line_4.append('│         │')
        line_5.append('│    {}    │'.format(suit))
        line_6.append('│         │')
        line_7.append('│         │')
        line_8.append('│        {}│'.format(rank))
        line_9.append('└─────────┘')

    result = ''.join(line_1) + '\n' + ''.join(line_2) + '\n' + ''.join(line_3) + '\n' + ''.join(line_4) + '\n' + ''.join(line_5) + '\n' + ''.join(line_6) + '\n' + ''.join(line_7) + '\n' + ''.join(line_8) + '\n' + ''.join(line_9)

    return result

test_card_1 = Card('Diamonds', '4')
test_card_2 = Card('Clubs', 'Ace')

print(convert_card_to_ascii(test_card_1, test_card_2))


