"""Command-line entry point for running a MoneyPoly game session."""

from moneypoly.game import Game


def get_player_names():
    """Prompt for and return a list of non-empty player names."""
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names



def main():
    """Create a Game instance from user input and start it."""
    names = get_player_names()
    try:
        game = Game(names)
        game.run()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except ValueError as exc:
        print(f"Setup error: {exc}")


if __name__ == "__main__":
    main()
