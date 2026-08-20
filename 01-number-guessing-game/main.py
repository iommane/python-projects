import random

# Generate a random target based on difficulty
def generate_target(level: str, start: int = 1) -> tuple[int, int]:
    if level == "easy":
        end = 10
    elif level == "medium":
        end = 100
    elif level == "hard":
        end = 1000
    else:
        raise ValueError("Invalid difficulty")

    target = random.randint(start, end)
    return target, end

# Validate user's guess againts the target
def validate_guess(target: int, entry: int) -> tuple[bool, str]:
    if entry == target:
        return True, "Correct!"
    if entry < target:
        return False, "Too low"
    return False, "Too high"

game_state = True

print("Welcome to guess the number game")

while game_state:
    guess_state = True
    attempts = 0

    try:
        level = input("Enter your difficulty level (easy, medium, hard): ").strip().lower()
        target, end = generate_target(level = level)
    except ValueError:
        print("Please enter valid level")
        continue
    except KeyboardInterrupt:
        print("Stopped")
        exit()
        
    while guess_state:
        try:
            entry = int(input(f"Guess number between 1 to {end} : "))
            attempts += 1
            valid_guess, message = validate_guess(target = target, entry = entry)
    
            if valid_guess:
                print(message)
                print("Total attempts:",attempts)
                guess_state = False
            else:
                print(message)

        except ValueError:
            print("Guess is invalid")
            continue
        except KeyboardInterrupt:
            print("Stopped")
            exit()

    try:
        retry = input("Want re-match? (yes/no) : ").strip().lower()
        if retry == "yes":
            continue
        elif retry == "no":
            game_state = False
        else:
            print("Invalid choice")
            game_state = False
    except KeyboardInterrupt:
        print("Stopped")
        exit()

print("Game end!")