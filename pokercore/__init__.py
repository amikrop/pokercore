"""pokercore

A poker engine core, in Python

pokercore provides 3 classes to be used in a poker engine.
Card (a playing card), Hand (a poker hand consisting of Cards,
with evaluation capabilities) and Deck (a deck of Cards).

It is a simple starter, mainly written for exploring purposes,
but can be extended and/or used to build something bigger. It is
released under the MIT license.

Example

>>> from pokercore import Deck, Hand
>>> deck = Deck()
>>> first = Hand(deck.draw(5))
>>> first
Hand(one pair: Card(9c), Card(9h), Card(Ac), Card(Jh), Card(2h))
>>> second = Hand(deck.draw(5))
>>> second
Hand(high card: Card(As), Card(Kc), Card(9s), Card(7h), Card(4h))
>>> first > second
True
"""

__title__ = 'pokercore'
__version__ = '0.1.4'
__author__ = 'Aristotelis Mikropoulos'

from pokercore.exceptions import *
from pokercore.card import Card
from pokercore.hand import Hand
from pokercore.deck import Deck
