import tkinter as tk
from tkinter import messagebox

from game.game1.game1deck import Deck
from game.game1.game1player import Player
from game.game1.game1round import Round
from game.game1.game1game import Game

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Card Game GUI")

        # Top frame: round, turn, & money
        top = tk.Frame(self.root)
        top.pack(pady=5, fill=tk.X)
        self.round_label = tk.Label(top, text="Round: 1", font=("Arial", 14))
        self.round_label.pack(side=tk.LEFT, padx=10)
        self.turn_label = tk.Label(top, text="Turn: Player 1", font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, padx=10)
        self.money_label = tk.Label(top, text="Money: $0", font=("Arial", 14))
        self.money_label.pack(side=tk.LEFT, padx=10)

        # Hand container (top)
        hand_container = tk.Frame(self.root)
        hand_container.pack(pady=5, fill=tk.X)
        hand_box = tk.LabelFrame(hand_container, text="Your Hand")
        hand_box.pack(padx=10, fill=tk.X)
        self.hand_frame = hand_box

        # Bench container (below hand)
        bench_container = tk.Frame(self.root)
        bench_container.pack(pady=5, fill=tk.X)
        bench1_box = tk.LabelFrame(bench_container, text="Bench: Player 1")
        bench1_box.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        bench2_box = tk.LabelFrame(bench_container, text="Bench: Player 2")
        bench2_box.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.bench_frames = [bench1_box, bench2_box]

        # Bottom frame: controls
        ctrl = tk.Frame(self.root)
        ctrl.pack(pady=5)
        tk.Button(ctrl, text="Redraw ($2)", command=self.on_redraw).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="End Turn", command=self.on_end).pack(side=tk.LEFT, padx=5)

        # internal state
        self.selected_idx = None
        self.action_var = tk.StringVar()

    def on_card_action(self, idx, action):
        self.selected_idx = idx
        self.action_var.set(action)

    def on_redraw(self):
        self.action_var.set("redraw")

    def on_end(self):
        self.action_var.set("end")

    def draw_cards(self, cards, frame, clickable=False, action=None):
        # Clear frame
        for w in frame.winfo_children():
            w.destroy()
        # Draw cards
        for i, c in enumerate(cards):
            txt = f"{c.name} (${c.value})"
            btn = tk.Button(frame, text=txt, width=10)
            if clickable and action:
                btn.config(command=lambda i=i, a=action: self.on_card_action(i, a))
            btn.pack(side=tk.LEFT, padx=2)

    def update_ui(self):
        # Update top labels
        self.round_label.config(text=f"Round: {self.current_round}")
        self.turn_label.config(text=f"Turn: {self.player.name}")
        self.money_label.config(text=f"Money: ${self.player.money}")

        # Draw hand: click to bench
        self.draw_cards(
            self.player.hand,
            self.hand_frame,
            clickable=True,
            action="bench"
        )
        # Draw benches: current player's bench clickable to sell
        for idx, pl in enumerate(self.game.players):
            action = None
            clickable = False
            if pl is self.player:
                action = "sell"
                clickable = True
            self.draw_cards(
                pl.bench,
                self.bench_frames[idx],
                clickable=clickable,
                action=action
            )

        self.root.update_idletasks()

    def take_turn(self, player, game):
        self.player = player
        self.game = game
        while True:
            self.current_round = game.round_number
            self.update_ui()
            self.action_var.set("")
            self.root.wait_variable(self.action_var)
            act = self.action_var.get()

            if act == "bench":
                idx = self.selected_idx
                card = player.hand.pop(idx)
                if player.money >= card.value:
                    player.money -= card.value
                    player.bench.append(card)
                else:
                    player.hand.insert(idx, card)

            elif act == "sell":
                idx = self.selected_idx
                card = player.bench.pop(idx)
                player.money += 1

            elif act == "redraw":
                cost = game.redraw_cost
                if player.money >= cost:
                    player.money -= cost
                    excluded = [c for p in game.players for c in p.bench]
                    player.hand = game.deck.draw(5, exclude_cards=excluded)

            elif act == "end":
                break

    def play_loop(self, num_rounds=3, starting_money=10):
        deck = Deck(2, 5, 10)
        players = [Player(f"Player {i+1}", starting_money) for i in range(2)]
        game = Game(
            deck,
            players,
            redraw_cost=2,
            interest_factor=2,
            money_per_round=5,
            low_value=2,
            medium_value=5,
            high_value=10,
            turns_per_round=2,
            triple_multiplier=3
        )

        for r in range(num_rounds):
            game.round_number = r + 1
            # Initial draw
            for p in players:
                excluded = [c for pl in players for c in pl.bench]
                p.hand = game.deck.draw(5, exclude_cards=excluded)
            # Player turns
            for p in players:
                self.take_turn(p, game)
            # Round results
            rnd = Round(game)
            winner = rnd.determine_round_winner()
            winner.rounds_won += 1
            # Summary
            vals = [pl.calculate_bench_value(game.triple_multiplier) for pl in players]
            msg = (
                f"Player 1 bench value: {vals[0]}\n"
                f"Player 2 bench value: {vals[1]}\n"
                f"Round {r+1} winner: {winner.name}"
            )
            messagebox.showinfo(f"Round {r+1} Results", msg)
            # Interest and payout
            for p in players:
                p.money = p.money * game.interest_factor + game.money_per_round

        # Game over
        self.round_label.config(text="Game Over")
        self.turn_label.config(text="")
        self.money_label.config(text=f"Winner: {game.determine_winner().name}")
        for w in self.root.winfo_children():
            if isinstance(w, tk.Button):
                w.config(state=tk.DISABLED)

    def run(self):
        self.play_loop()
        self.root.mainloop()

if __name__ == "__main__":
    gui = GameGUI()
    gui.run()