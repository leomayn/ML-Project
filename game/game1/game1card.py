# A card has a rank, suit, and value.
# game/game1/game1card.py

class Card:
    def __init__(self, name: str, value: int):
        self.name = name      # e.g. "2s", "3s", "Jh", ...
        self.value = value    # e.g. low_value, medium_value, high_value

    def __repr__(self):
        # shows both type and value
        return f"{self.name}(${self.value})"

    def __eq__(self, other):
        return isinstance(other, Card) and self.name == other.name and self.value == other.value

    def __hash__(self):
        return hash((self.name, self.value))
