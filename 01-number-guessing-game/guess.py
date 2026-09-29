import random

LEVELS = {
    "easy":   {"range": (1, 10),  "attempts": 5},
    "medium": {"range": (1, 50),  "attempts": 10},
    "hard":   {"range": (1, 100), "attempts": 20},
}


class Guess:
    def __init__(self, difficulty: str):
        if difficulty not in LEVELS:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        config = LEVELS[difficulty]
        self.low, self.high = config["range"]
        self.total_attempts = config["attempts"]
        self.secret_number = random.randint(self.low, self.high)
        self.attempts = 0
        self.is_over = False
        self.is_won = False

    def guess(self, number: int) -> str:
        if not self.low <= number <= self.high:
            raise ValueError(f"Please enter a number between {self.low} and {self.high}")

        self.attempts += 1

        if number == self.secret_number:
            self.is_over = True
            self.is_won = True
            return f"🎉 Correct! You guessed it in {self.attempts} attempts!"

        if self.attempts >= self.total_attempts:
            self.is_over = True
            return f"💀 Out of attempts! The number was {self.secret_number}."

        hint = "higher" if number < self.secret_number else "lower"
        return f"Try a {hint} number\nRemaining attempts: {self.total_attempts - self.attempts}"