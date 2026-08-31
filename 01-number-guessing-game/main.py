import random


class GuessGame:
    def __init__(self):
        self.target: int = 0
        self.end_number: int = 0
        self.attempts: int = 0
        self.difficulty: str = None
        self.levels: dict = {"easy": 10, "medium": 100, "hard": 1000}

    def set_difficulty(self) -> None:
        print("\nChoose difficulty:\n- Easy\n- Medium\n- Hard")

        while True:
            level = input("Enter level you want to play: ").strip().lower()

            if level in self.levels:
                self.difficulty = level
                self.end_number = self.levels[level]
                break
            else:
                print("🚫 Invalid difficulty")

    def generate_target(self) -> None:
        self.target = random.randint(1, self.end_number)

    def get_guess(self) -> int:
        while True:
            try:
                guess = int(input(f"🤔 Enter your guess 1-{self.end_number}: "))

                if 1 <= guess <= self.end_number:
                    return guess
                else:
                    print(f"❌ Please enter a number between 1 and {self.end_number}")

            except ValueError:
                print("🚫 Invalid input")

    def check_guess(self, guess: int) -> bool:
        return guess == self.target

    def get_hint(self, guess: int) -> None:
        if guess < self.target:
            print("Too low")
        else:
            print("Too high")

    def play(self) -> None:
        print("🎮 Welcome to the Number Guessing Game!")

        while True:
            self.attempts = 0
            self.set_difficulty()
            self.generate_target()

            while True:
                guess = self.get_guess()
                self.attempts += 1

                if self.check_guess(guess):
                    print(
                        f"🎉 Correct! You guessed the number in {self.attempts} attempts!"
                    )
                    break
                else:
                    self.get_hint(guess)

            if not self.retry():
                print("Game over")
                break

    def retry(self) -> bool:
        while True:
            is_retry = input("\nWant to play again? (y/n): ").strip().lower()

            if is_retry == "y":
                return True
            elif is_retry == "n":
                return False
            else:
                print("🫩 Invalid input. Please enter 'y' or 'n'")


if __name__ == "__main__":
    try:
        game = GuessGame()
        game.play()

    except KeyboardInterrupt:
        print("\nGame stopped")

    finally:
        print("Thank you for playing")
