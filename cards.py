import enum
import random
from dataclasses import dataclass


class Rank(enum.Enum):
    ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING = range(1, 14)

    @property
    def abbr(self):
        return '0A23456789TJQK'[self.value]

    @property
    def point(self):
        return min(10, self.value)  # J, Q, K counts as 10


class Suit(enum.Enum):
    CLUB, DIAMOND, HEART, SPADE = range(1, 5)

    @property
    def suit_symbol(self):
        return {
            1: '\u2663',
            2: '\u2662',
            3: '\u2661',
            4: '\u2660',
        }[self.value]

@dataclass
class Card(object):
    rank: Rank
    suit: Suit

    def __repr__(self):
        return self.rank.abbr + self.suit.suit_symbol

class Deck(list):
    def __init__(self, number_of_decks = 6):
        list.__init__(self, [Card(rank, suit) for rank in Rank
                             for suit in Suit
                             for _ in range(number_of_decks)])
        random.shuffle(self)



if __name__ == '__main__':
    d = Deck()

