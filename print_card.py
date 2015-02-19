from blackjack import Card

def convert_card_to_ascii(*cards):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
        # get the cards suit in two steps
        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}        │'.format(rank))
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│        {}│'.format(rank))
        lines[8].append('└─────────┘')

    # result = ''.join(line_1) + '\n' + ''.join(line_2) + '\n' + ''.join(line_3) + '\n' + ''.join(line_4) + '\n' + ''.join(line_5) + '\n' + ''.join(line_6) + '\n' + ''.join(line_7) + '\n' + ''.join(line_8) + '\n' + ''.join(line_9)
    result = ''
    for index, line in enumerate(lines):
        result += ''.join(lines[index]) + '\n'

    return result

test_card_1 = Card('Diamonds', '4')
test_card_2 = Card('Clubs', 'Ace')
test_card_3 = Card('Spades', 'Jack')
test_card_4 = Card('Hearts', '10')

print(convert_card_to_ascii(test_card_1, test_card_2, test_card_3, test_card_4))


