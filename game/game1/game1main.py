# Game rules: the game consists of a standard deck of 52 cards.
# 2-10 are low value, J-K are medium value, and A is high value.
# Each player starts with the same amount of money.
# The game consists of an odd number of rounds.
# Each round begins by each player drawing 5 cards from the deck.
# Players take turns.
# During the turn they can choose cards from their hand to add to their bench.
# Adding a card to the bench costs the value of the card.
# Players can redraw cards from the deck, but it costs money.
# After players completed their turns, player with the three highest value cards in their bench wins the round.
# Having three cards of the same rank can count as one card of the cards value times a multiplier
# At the end of each round, players money is multiplied by the interest factor.
# Players keep their bench for the next round.
# Players can sell cards from their bench for 1 dollar each.
# After the last round, the player with the most rounds won is the overall winner.

# game/game1/game1main.py

from game.game1.game1deck import Deck
from game.game1.game1player import Player
from game.game1.game1game import Game
from game.game1.game1round import Round


def main():
    # --- CONFIGURATION ---
    low_value = 1
    medium_value = 5
    high_value = 10

    redraw_cost = 2
    interest_factor = 2
    money_per_round = 5  # money added to each player at end of round
    turns_per_round = 2
    triple_multiplier = 3  # triple of same card counts as value * multiplier

    player_names = ["Alice", "Bob"]
    starting_money = 10
    num_rounds = 3
    # ----------------------

    # Initialize deck and players
    deck = Deck(low_value, medium_value, high_value)
    players = [Player(name, starting_money) for name in player_names]

    # Pass triple_multiplier into the game
    game = Game(
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
    )

    rnd = Round(game)
    for r in range(num_rounds):
        print(f"\n=== Round {r+1} ===")
        rnd.play_round()

    winner = game.determine_winner()
    print(f"\n=== Game Over ===\nGame Winner: {winner.name} (rounds won = {winner.rounds_won})")


if __name__ == "__main__":
    main()