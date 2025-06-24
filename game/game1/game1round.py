# The round starts of by choosing a player to start.
# The player can buy cards from their hand to their bench.
# The player can also redraw cards from the deck, but it costs money.
# After the player has finished their turn, the next player can do the same.
# Repeat this until each player has had a certain number of turns.
# After all players have had their turns, the player with the three highest value cards in their bench wins the round.
# If a player has three cards of the same rank, they can count it as one card of the value times a multiplier.
# At the end of the round, players money is multiplied by the interest factor.
# Players keep their bench for the next round.

class Round:
    def __init__(self, game):
        self.game = game

    def play_round(self):
        # --- FREE redraw at start of round ---
        for player in self.game.players:
            player.hand.clear()
            bench_cards = [c for p in self.game.players for c in p.bench]
            new = self.game.deck.draw(5, exclude_cards=bench_cards)
            player.hand.extend(new)
            print(f"{player.name} drew {new}")

        # --- Interleaved turns: P1, P2, … repeat ---
        for turn_num in range(1, self.game.turns_per_round + 1):
            for player in self.game.players:
                print(f"\n{player.name}'s turn ({turn_num}/{self.game.turns_per_round}):")
                player.take_turn(self.game)

        # Determine and record this round’s winner
        round_winner = self.determine_round_winner()
        value = round_winner.calculate_bench_value(self.game.triple_multiplier)
        round_winner.rounds_won += 1
        print(
            f"\nRound Winner: {round_winner.name} ``(bench value = {value})``"
        )

        # Apply interest to all players
        for player in self.game.players:
            player.money *= self.game.interest_factor
            player.money += self.game.money_per_round

    def determine_round_winner(self):
        return max(
            self.game.players,
            key=lambda p: p.calculate_bench_value(self.game.triple_multiplier)
        )



