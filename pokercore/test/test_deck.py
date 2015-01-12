from unittest import TestCase

from pokercore.card import Card
from pokercore.deck import Deck, DeckNotIntegerError, DeckTooManyError


class TestDeck(TestCase):

    def test_create(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(deck.remaining), 52)
        for i in xrange(52):
            self.assertIsInstance(deck.cards[i], Card)
            self.assertIsInstance(deck.remaining[i], Card)
        self.assertEqual(sorted(deck.cards), sorted(set(deck.cards)))
        self.assertEqual(sorted(deck.remaining), sorted(set(deck.remaining)))

    def test_draw(self):
        deck = Deck()
        self.assertRaises(DeckNotIntegerError, deck.draw, '7')
        self.assertRaises(DeckTooManyError, deck.draw, 53)

        card = deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.remaining), 51)

        cards = deck.draw(4)
        for c in cards:
            self.assertIsInstance(c, Card)
            for r in deck.remaining:
                self.assertFalse(c.identical_to(r))
        self.assertEqual(len(cards), 4)
        self.assertEqual(len(deck.remaining), 47)

    def test_shuffle(self):
        deck = Deck()
        deck.draw(10)
        deck.shuffle()
        self.assertEqual(len(deck.remaining), 52)