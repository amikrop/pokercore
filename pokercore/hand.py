from operator import attrgetter

from pokercore.exceptions import HandCreationError, HandComparisonError
from pokercore.card import Card, CardCreationError


class Hand(object):
    """Class representing a poker hand.

    A poker hand consists of one or more Card objects, passed to the
    constructor contained in some iterable. Its main attributes are two:

    * value - an integer between 0 and 8 representing the category of
              the poker hand
    * best_cards - the best (at most 5) cards that consist the actual hand

    A Hand can be compared to other Hand objects, judging by the value,
    and then the best cards, lexicographically.
    """

    names = ('high card',
             'one pair',
             'two pair',
             'three of a kind',
             'straight',
             'flush',
             'full house',
             'four of a kind',
             'straight flush')

    def __init__(self, cards):
        self.cards = list(cards)
        if not self.cards:
            raise HandCreationError('cannot create empty hand')

        for c in self.cards:
            if not isinstance(c, Card):
                raise HandCreationError('hand can only consist of cards')

        self.value, self.best_cards = self._evaluate()

    def __repr__(self):
        return 'Hand(%s: %s)' % (self.names[self.value],
                                 ', '.join(str(c) for c in self.best_cards))

    def _find_straight(self, cards):
        """find highest possible straight in given uniquely ranked cards"""

        connections = 0
        current = cards[0]
        for i in xrange(1, len(cards)):
            if current == cards[i] + 1:
                connections += 1
                if connections == 4:
                    return cards[i - 4:i + 1]
            else:
                connections = 0
            current = cards[i]

        possible = cards[-4:] + [cards[0]]
        if possible == [3, 2, 1, 0, 12]:
            return possible
        return []

    def _max_group(self, length, *excluded, **kwargs):
        """find highest-ranked group of equally ranked cards,
        with minimum length as the one given
        """

        result = []
        for g in self._groups:
            if len(g) >= length and g[0] not in excluded and g > result:
                result = g[:5]

        if kwargs.get('one'):
            result = result[:1]

        return result

    def _kickers(self, n, *excluded):
        """find at most n unequally ranked kickers"""

        result = []
        for i in xrange(n):
            result.extend(self._max_group(1,
                                          *(result + list(excluded)),
                                          one=True))
        return result

    def _evaluate(self):
        """evaluate the kind of the hand and find the best cards"""

        # straight flush (checking also for flush)
        cards = sorted(self.cards, key=attrgetter('suit', 'rank'),
                       reverse=True)
        by_suit = []
        suit = -1
        for c in cards:
            if c.suit != suit:
                by_suit.append([])
                suit = c.suit
            by_suit[-1].append(c)

        flush = []
        straight_flush = []
        for suited in by_suit:
            if len(suited) >= 5:
                if suited > flush:
                    flush = suited[:5]
                straight_flush = max(self._find_straight(suited),
                                     straight_flush)

        if straight_flush:
            return 8, straight_flush

        # group equally ranked cards
        groups = {}
        for c in self.cards:
            groups.setdefault(c.rank, []).append(c)
        self._groups = groups.values()

        # four of a kind
        four_of_a_kind = self._max_group(4)
        if four_of_a_kind:
            return 7, four_of_a_kind + self._kickers(1, four_of_a_kind[0])

        # full house (checking also for three of a kind)
        three_of_a_kind = self._max_group(3)
        if three_of_a_kind:
            pair = self._max_group(2, three_of_a_kind[0])
            if pair:
                return 6, three_of_a_kind + pair

        # flush
        if flush:
            return 5, flush

        # straight
        uniquely_ranked = []
        unique_ranks = set()
        for c in sorted(self.cards, reverse=True):
            if c.rank not in unique_ranks:
                uniquely_ranked.append(c)
                unique_ranks.add(c.rank)

        straight = self._find_straight(uniquely_ranked)
        if straight:
            return 4, straight

        # three of a kind
        if three_of_a_kind:
            return 3, three_of_a_kind + self._kickers(2, three_of_a_kind[0])

        # pairs
        pair = self._max_group(2)
        if pair:
            second_pair = self._max_group(2, pair[0])
            if second_pair:
                # two pair
                return 2, (pair + second_pair +
                           self._kickers(1, pair[0], second_pair[0]))
            # one pair
            return 1, pair + self._kickers(3, pair[0])

        # high card
        return 0, uniquely_ranked[:5]

    def __cmp__(self, other):
        if not isinstance(other, Hand):
            raise HandComparisonError('cannot compare hand to non-hand')

        return cmp((self.value, self.best_cards),
                   (other.value, other.best_cards))

    @classmethod
    def from_chars(cls, *args):
        """return a new object from pairs of character symbols

        works with either multiple arguments, or a single iterable
        """

        try:
            return cls(Card.from_chars(chars) for chars in args)
        except CardCreationError:
            try:
                return cls(Card.from_chars(chars) for chars in args[0])
            except (TypeError, CardCreationError):
                pass
            raise HandCreationError('invalid card symbols')