def ascii_card(suit=False, rank=False):
    """
    Instead of a boring text version of the card we render an ASCII card
    :param suit: string, e.g Hearths
    :param rank: string, e.g King or 3
    """


    if suit and rank:  # used to see if the card should be hidden, aka the dealers 1st card,or instead of and as a backup
        # the card should be shown
        suit = ['Spades', 'Diamonds', 'Hearts', 'Clubs'].index(suit)  # turn suit into a number, index of suit
        suit = ['♠', '♦', '♥', '♣'][suit]
        result = '┌─────────┐\n│{1}        │\n│         │\n│         │\n│    {0}    │\n│         │\n│         │\n│        {1}│\n└─────────┘'.format(suit, rank)
    else:  # hidden card
         result = '┌─────────┐\n│░░░░░░░░░│\n│░░░░░░░░░│\n│░░░░░░░░░│\n│░░░░░░░░░│\n│░░░░░░░░░│\n│░░░░░░░░░│\n│░░░░░░░░░│\n└─────────┘\n'
    return result

print(ascii_card('Hearts', 2))


