from game import Game

def main():
    try:
        Game().play()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

if __name__ == "__main__":
    main()