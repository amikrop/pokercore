from unittest import TestCase

from pokercore.card import (Card,
                            CardCreationError,
                            CardArithmeticError,
                            CardComparisonError)


class TestCard(TestCase):

    def test_create(self):
        self.assertRaises(CardCreationError, Card, '3', 2)
        self.assertRaises(CardCreationError, Card, 9, 'H')
        self.assertRaises(CardCreationError, Card, 3, 5)
        self.assertRaises(CardCreationError, Card, 13, 0)
        self.assertRaises(CardCreationError, Card.from_chars, '51')
        self.assertRaises(CardCreationError, Card.from_chars, '10S')

        card = Card(3, 2)
        self.assertIsInstance(card, Card)
        self.assertEqual(card.rank, 3)
        self.assertEqual(card.suit, 2)

        card = Card.from_chars('TC')
        self.assertIsInstance(card, Card)
        self.assertEqual(card.rank, 8)
        self.assertEqual(card.suit, 0)

    def test_arithmetic(self):
        first = Card.from_chars('8D')
        self.assertRaises(TypeError, lambda c: c * 4, first)
        self.assertRaises(TypeError, lambda c: 1 * c, first)
        self.assertRaises(TypeError, lambda c: c / 2, first)
        self.assertRaises(TypeError, lambda c: 8 / c, first)
        self.assertRaises(CardArithmeticError, lambda c: c + '3', first)
        self.assertRaises(CardArithmeticError, lambda c: c - '1', first)

        self.assertEqual(first + 3, 9)
        self.assertEqual(2 + first, 8)
        self.assertEqual(first - 4, 2)
        self.assertEqual(10 - first, 4)

        second = Card(2, 2)
        self.assertRaises(TypeError, lambda c: c * second, first)
        self.assertRaises(TypeError, lambda c: second / c, first)
        self.assertEqual(first + second, 8)
        self.assertEqual(first - second, 4)
        self.assertEqual(second + 3 - first, -1)
        self.assertEqual(10 - second + first, 14)

    def test_compare(self):
        first = Card(9, 2)
        self.assertRaises(CardComparisonError, lambda c: c > 'A', first)
        self.assertRaises(CardComparisonError, lambda c: 't' <= c, first)
        self.assertRaises(CardComparisonError, lambda c: c == '9', first)
        self.assertRaises(CardComparisonError, lambda c: c != 'j', first)
        self.assertRaises(CardComparisonError, first.identical_to, 9)

        second = Card(11, 1)
        self.assertNotEqual(first, second)
        self.assertLess(first, second)
        self.assertLessEqual(first, second)
        self.assertGreater(second, first)
        self.assertGreaterEqual(second, first)
        self.assertFalse(first.identical_to(second))

        second = Card.from_chars('js')
        self.assertEqual(first, second)
        self.assertFalse(second.identical_to(first))

        second = Card.from_chars('Jh')
        self.assertEqual(second, first)
        self.assertTrue(first.identical_to(second))

        self.assertEqual(first, 9)
        self.assertLess(first, 11)
        self.assertLessEqual(first, 12)
        self.assertGreater(first, 2)
        self.assertGreaterEqual(first, 9)