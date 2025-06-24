# The deck consistists of some number of cards
# Each card has a rank, suit, and value
# The values of the cards are passed in from the game
# The deck can be shuffled and cards can be drawn from it
# game/game1/game1deck.py

import random
from game.game1.game1card import Card

class Deck:
    DEFAULT_LOW_TYPES    = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
    DEFAULT_MEDIUM_TYPES = ["J", "Q", "K"]
    DEFAULT_HIGH_TYPES   = ["A"]

    def __init__(
        self,
        low_value: int,
        medium_value: int,
        high_value: int,
        low_types:    list[str] | None = None,
        medium_types: list[str] | None = None,
        high_types:   list[str] | None = None,
    ):
        # choose which “names” go with each tier
        self.low_types    = low_types    or Deck.DEFAULT_LOW_TYPES
        self.medium_types = medium_types or Deck.DEFAULT_MEDIUM_TYPES
        self.high_types   = high_types   or Deck.DEFAULT_HIGH_TYPES

        # store ONE prototype per card‐type
        self._prototypes: list[Card] = []
        for t in self.low_types:
            self._prototypes.append(Card(t, low_value))
        for t in self.medium_types:
            self._prototypes.append(Card(t, medium_value))
        for t in self.high_types:
            self._prototypes.append(Card(t, high_value))

    def draw(self, num: int, exclude_cards: list[Card] | None = None) -> list[Card]:
        """
        Sample with replacement from the full prototype set,
        excluding any names present in exclude_cards (i.e. bench cards).
        """
        exclude_names = {c.name for c in (exclude_cards or [])}
        available = [c for c in self._prototypes if c.name not in exclude_names]
        if not available:
            raise ValueError("No cards available to draw (all are excluded).")
        chosen = random.choices(available, k=num)
        # return fresh instances
        return [Card(c.name, c.value) for c in chosen]

    def shuffle(self):
        # no-op under replacement logic
        pass

    def add_cards(self, cards: list[Card]):
        # no-op under replacement logic
        pass
