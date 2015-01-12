from pokercore.exceptions import (CardCreationError,
                                  CardArithmeticError, CardComparisonError)


class Card(object):
    """Class representing a playing card.

    A playing card consists of two integers, passed to the constructor during
    instantiation:

    * rank - the rank of the card [0-12]
    * suit - the suit of the card [0-3]

    A Card can be compared to, added to, subtracted to and subtracted by
    other Card objects and integers (using their ranks, resulting in plain
    integers). For identity check, the identical_to method is provided.
    """

    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
    suits = ('c', 'd', 'h', 's')

    def __init__(self, rank, suit):
        if rank not in xrange(13):
            raise CardCreationError('card rank must lie between'
                                    '0 and 12, inclusive')

        if suit not in xrange(4):
            raise CardCreationError('card suit must lie between'
                                    '0 and 3, inclusive')

        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return 'Card(%s%s)' % (self.ranks[self.rank], self.suits[self.suit])

    def __add__(self, other):
        if isinstance(other, int):
            return self.rank + other

        if isinstance(other, Card):
            return self.rank + other.rank

        raise CardArithmeticError('cards can only be added'
                                  'to cards and integers')

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int):
            return self.rank - other

        if isinstance(other, Card):
            return self.rank - other.rank

        raise CardArithmeticError('cards can only be subtracted'
                                  'by cards and integers')

    def __rsub__(self, other):
        if isinstance(other, int):
            return other - self.rank

        if isinstance(other, Card):
            return other.rank - self.rank

        raise CardArithmeticError('cards can only subtract'
                                  'cards and integers')

    def __cmp__(self, other):
        if isinstance(other, Card):
            return cmp(self.rank, other.rank)

        if isinstance(other, int):
            return cmp(self.rank, other)

        raise CardComparisonError('cards can only be compared'
                                  'to cards and integers')

    def identical_to(self, other):
        if not isinstance(other, Card):
            raise CardComparisonError('cannot identity-check card'
                                      'with non-card')

        return (self.rank, self.suit) == (other.rank, other.suit)

    @classmethod
    def from_chars(cls, chars):
        """return a new object from a pair of character symbols"""

        try:
            if len(chars) != 2:
                raise CardCreationError('invalid card symbols')

            rank = chars[0].upper()
            suit = chars[1].lower()
            return cls(cls.ranks.index(rank), cls.suits.index(suit))

        except (TypeError, AttributeError, ValueError):
            raise CardCreationError('invalid card symbols')