class DominoesScorer:
    def __init__(self):
        self.players = []
        self.scores = {}
        self.rounds = ['12s', '11s', '10s', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s', '1s', 'Blanks']
        self.current_round = 0
        self.round_scores = {}

    def setup_game(self):
        """Set up the game by getting player count and names"""
        print("=== DOMINOES SCORE KEEPER ===")
        print()

        while True:
            try:
                num_players = int(input("How many players? "))
                if num_players < 2:
                    print("Need at least 2 players!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")

        print()
        for i in range(num_players):
            while True:
                name = input(f"Enter name for player {i + 1}: ").strip()
                if name:
                    self.players.append(name)
                    self.scores[name] = 0
                    break
                print("Please enter a valid name!")

        print(f"\nPlayers: {', '.join(self.players)}")
        print(f"Game will progress through: {' → '.join(self.rounds)}")
        print("Lowest total score wins!")
        print()

    def display_current_standings(self):
        """Display current game standings"""
        print("\n=== CURRENT STANDINGS ===")
        sorted_players = sorted(self.players, key=lambda p: self.scores[p])

        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player}: {self.scores[player]} points")
        print()

    def play_round(self):
        """Play a single round"""
        if self.current_round >= len(self.rounds):
            return False

        round_name = self.rounds[self.current_round]
        print(f"=== ROUND {self.current_round + 1}: {round_name} ===")

        # Get winner first
        print("Who went out first (winner)?")
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player}")

        while True:
            try:
                winner_choice = int(input("Enter winner number: ")) - 1
                if 0 <= winner_choice < len(self.players):
                    winner = self.players[winner_choice]
                    break
                print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")

        print(f"\n{winner} went out first and gets 0 points!")

        # Initialize round scores
        self.round_scores = {player: 0 for player in self.players}
        self.round_scores[winner] = 0

        # Get pip counts for other players
        print("\nEnter pip count for remaining players:")
        for player in self.players:
            if player != winner:
                while True:
                    try:
                        pips = int(input(f"{player}'s remaining pips: "))
                        if pips >= 0:
                            self.round_scores[player] = pips
                            break
                        print("Pip count cannot be negative!")
                    except ValueError:
                        print("Please enter a valid number!")

        # Update total scores
        print(f"\n--- ROUND {self.current_round + 1} RESULTS ---")
        for player in self.players:
            round_score = self.round_scores[player]
            self.scores[player] += round_score
            print(f"{player}: +{round_score} (Total: {self.scores[player]})")

        self.current_round += 1
        return True

    def show_final_results(self):
        """Show final game results"""
        print("\n" + "=" * 40)
        print("FINAL RESULTS")
        print("=" * 40)

        # Sort players by total score (lowest wins)
        sorted_players = sorted(self.players, key=lambda p: self.scores[p])

        for i, player in enumerate(sorted_players, 1):
            if i == 1:
                print(f"🏆 WINNER: {player} with {self.scores[player]} points!")
            else:
                print(f"{i}. {player}: {self.scores[player]} points")

        print("\nThanks for playing!")

    def run_game(self):
        """Run the complete game"""
        self.setup_game()

        while True:
            if not self.play_round():
                break

            self.display_current_standings()

            if self.current_round < len(self.rounds):
                continue_game = input("Continue to next round? (y/n): ").lower().strip()
                if continue_game != 'y':
                    break

        self.show_final_results()


def main():
    game = DominoesScorer()
    game.run_game()


if __name__ == "__main__":
    main()
