from os.path import dirname, join
from unittest import TestCase

from pokercore.card import Card
from pokercore.hand import Hand, HandCreationError, HandComparisonError


class TestHand(TestCase):

    def setUp(self):
        self.players = [], []
        self.wins = []
        with open(join(dirname(__file__), 'testcases')) as testcases:
            for i, line in enumerate(testcases):
                case = i % 3
                parts = line.split()
                if case == 2:
                    self.wins.append(int(parts[0]))
                else:
                    self.players[case].append((Hand.from_chars(parts[:-1]),
                                               int(parts[-1])))

    def test_create(self):
        self.assertRaises(TypeError, Hand, Card(1, 2))
        self.assertRaises(HandCreationError, Hand, [])
        self.assertRaises(HandCreationError, Hand, [3, 1])

        self.assertRaises(HandCreationError, Hand.from_chars)
        self.assertRaises(HandCreationError, Hand.from_chars, 4)
        self.assertRaises(HandCreationError, Hand.from_chars, 'aS', '4p')
        self.assertRaises(HandCreationError, Hand.from_chars, ['Th', 9])
        self.assertRaises(HandCreationError, Hand.from_chars,
                          'KH', 'Qs', 'Acd')

        hand = Hand([Card(4, 2), Card.from_chars('AS'), Card(9, 0)])
        self.assertIsInstance(hand, Hand)
        self.assertEqual(hand.value, 0)
        self.assertEqual(Hand.names[hand.value], 'high card')
        self.assertEqual(hand.best_cards, [12, 9, 4])

        hand = Hand.from_chars('4s', 'Th', '3s', '3c', 'Js', '3d')
        self.assertIsInstance(hand, Hand)
        self.assertEqual(hand.value, 3)
        self.assertEqual(Hand.names[hand.value], 'three of a kind')
        self.assertEqual(hand.best_cards, [1, 1, 1, 9, 8])

        hand = Hand.from_chars(['KH', '9H', 'KS', '9C'])
        self.assertIsInstance(hand, Hand)
        self.assertEqual(hand.value, 2)
        self.assertEqual(Hand.names[hand.value], 'two pair')
        self.assertEqual(hand.best_cards, [11, 11, 7, 7])

    def test_value(self):
        for i in xrange(0, 2):
            for h in self.players[i]:
                self.assertEqual(h[0].value, h[1])

    def test_compare(self):
        hand = Hand([Card.from_chars('Qc'), Card(1, 3)])
        self.assertRaises(HandComparisonError, lambda h: h < Card(5, 2), hand)
        self.assertRaises(HandComparisonError, lambda h: h >= 0, hand)
        self.assertRaises(HandComparisonError, lambda h: h != 'Qc', hand)
        self.assertRaises(HandComparisonError, lambda h: h == 10, hand)
        self.assertEqual(hand, hand)

        for i in xrange(len(self.players[0])):
            first = self.players[0][i][0]
            second = self.players[1][i][0]
            self.assertEqual(cmp(first, second), self.wins[i])