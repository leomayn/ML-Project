from collections import defaultdict

class Player:
    def __init__(self, name: str, starting_money: int):
        self.name = name
        self.money = starting_money
        self.hand: list = []
        self.bench: list = []
        self.rounds_won = 0

    def draw_cards(self, num, deck):
        new_cards = deck.draw(num)
        self.hand.extend(new_cards)
        print(f"{self.name} drew {new_cards}")

    def calculate_bench_value(self, triple_multiplier: int = 1) -> int:
        # Count cards by name
        counts = defaultdict(int)
        # Map name to value (all cards of same name have same value)
        values = {}
        for card in self.bench:
            counts[card.name] += 1
            values[card.name] = card.value

        # Build a list of contributions
        contributions = []
        for name, cnt in counts.items():
            val = values[name]
            if cnt >= 3:
                # One triple contribution
                contributions.append(val * triple_multiplier)
            else:
                # Each card contributes its value
                contributions.extend([val] * cnt)

        # Sum the top 3 contributions
        contributions.sort(reverse=True)
        return sum(contributions[:3])

    def sell_from_bench(self):
        if not self.bench:
            print("  Nothing to sell.")
            return
        print("  Bench:", list(enumerate(self.bench)))
        idx = int(input("  Which index to sell? "))
        card = self.bench.pop(idx)
        self.money += 1
        print(f"  Sold {card} for $1. Money now ${self.money}.")

    def take_turn(self, game):
        cost = game.redraw_cost

        print("\n  All benches:")
        for p in game.players:
            print(f"    {p.name}: {p.bench}")

        while True:
            print(f"\n  Your hand: {list(enumerate(self.hand))}")
            print(f"  Your bench: {self.bench}")
            print(f"  Money: ${self.money}")
            print("  [1] Bench a card")
            print("  [2] Redraw your entire hand for $2")
            print("  [3] Sell from bench")
            print("  [4] End turn")
            choice = input("  Choose an action: ")

            if choice == "1":
                idx = int(input("    Index in hand to bench: "))
                card = self.hand.pop(idx)
                if self.money >= card.value:
                    self.money -= card.value
                    self.bench.append(card)
                    print(f"    Benched {card} for ${card.value}.")
                else:
                    print("    Not enough money; card returned.")
                    self.hand.insert(idx, card)

            elif choice == "2":
                if self.money >= cost:
                    self.money -= cost
                    bench_cards = [c for p in game.players for c in p.bench]
                    self.hand = game.deck.draw(5, exclude_cards=bench_cards)
                    print(f"    Redrew hand for ${cost}. New hand: {self.hand}.")
                else:
                    print("    Not enough money to redraw.")

            elif choice == "3":
                self.sell_from_bench()

            elif choice == "4":
                break

            else:
                print("    Invalid choice—try again.")