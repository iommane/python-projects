from guess import Guess, LEVELS


class Game:
    def __init__(self):
        self.running = True
        self.result = {"win" : 0, "loss": 0}

    def menu(self) -> None:
        options = "\n".join(f"- {name.title()}" for name in LEVELS)
        print(f"Choose difficulty\n{options}")

    def set_difficulty(self) -> str:
        while True:
            difficulty = input("> ").strip().lower()
            if difficulty in LEVELS:
                return difficulty
            print("Invalid difficulty")

    def ask_restart(self) -> bool:
        while True:
            choice = input("Want to play again (yes/no)? ").strip().lower()
            if choice in ("yes", "no"):
                return choice == "yes"
            print("Invalid option")

    def get_summary(self) -> None:
        win, loss =self.result["win"], self.result["loss"]
        print("\n== Summary ==\n"
            f"Games played: {win + loss}\n"
            f"Win: {win}\n"
            f"Loss: {loss}")

    def play_round(self, round_: Guess) -> None:
        while not round_.is_over:
            raw = input("\nyour guess > ").strip()
            try:
                print(round_.guess(int(raw)))
            except ValueError as e:
                print(e)

        self.result["win" if round_.is_won else "loss"] += 1

    def play(self) -> None:
        print("==== Guess Game ====")
        while self.running:
            self.menu()
            self.play_round(Guess(self.set_difficulty()))
            self.running = self.ask_restart()
        self.get_summary()