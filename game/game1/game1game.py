# a game consists of a deck of cards and players
# game/game1/game1game.py

class Game:
    def __init__(
        self,
        deck,
        players,
        redraw_cost,
        interest_factor,
        money_per_round,
        low_value,
        medium_value,
        high_value,
        turns_per_round,
        triple_multiplier
    ):
        self.deck = deck
        self.players = players
        self.redraw_cost = redraw_cost
        self.interest_factor = interest_factor
        self.money_per_round = money_per_round
        self.low_value = low_value
        self.medium_value = medium_value
        self.high_value = high_value
        self.turns_per_round = turns_per_round
        self.triple_multiplier = triple_multiplier

    def determine_winner(self):
        # overall winner is whoever won the most rounds
        return max(self.players, key=lambda p: p.rounds_won)
