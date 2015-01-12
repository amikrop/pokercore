import random

from pokercore.exceptions import DeckNotIntegerError, DeckTooManyError
from pokercore.card import Card


class Deck(object):
    """Class representing a deck of cards.

    A Deck consists of 52 Card objects, starting shuffled.
    It has two methods:

    * shuffle - Restore all cards to the deck, then shuffle it.
    * draw - Draw n cards from the top of the deck, returning them
             as a list of Card objects. If n is not provided, draw
             and return one Card object.
    """

    def __init__(self):
        self.cards = [Card(r, s) for r in xrange(13) for s in xrange(4)]
        self.shuffle()

    def shuffle(self):
        """restore all cards to deck, then shuffle it"""

        self.remaining = list(self.cards)
        random.shuffle(self.remaining)

    def draw(self, n=None):
        """remove and return a card from the deck,
        or a list of n cards, if n is given
        """

        if n is None:
            return self.remaining.pop()

        if not isinstance(n, int):
            raise DeckNotIntegerError('draw count must be an integer')

        if n > len(self.remaining):
            raise DeckTooManyError('cannot draw more than remaining')

        return [self.remaining.pop() for i in xrange(n)]