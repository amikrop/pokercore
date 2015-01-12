"""pokercore

A poker engine core, in Python

pokercore provides 3 classes to be used in a poker engine.
Card (a playing card), Hand (a poker hand consisting of Cards,
with evaluation capabilities) and Deck (a deck of Cards).

Its is a simple starter, mainly written for exploring purposes,
but can be extended and/or used to build something bigger. It is
released under the MIT license.
"""

__title__ = 'pokercore'
__version__ = '0.1.3'
__author__ = 'Aristotelis Mikropoulos'

from pokercore.exceptions import *
from pokercore.card import Card
from pokercore.hand import Hand
from pokercore.deck import Deck
