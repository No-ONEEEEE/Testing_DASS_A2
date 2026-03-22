"""Entry point for running a MoneyPoly game from the command line."""

from moneypoly.game import Game


def get_player_names():
    """Prompt for and return a cleaned list of player names."""
    print("Enter player names separated by commas (minimum 2 players):")
    raw = input("> ").strip()
    names = [n.strip() for n in raw.split(",") if n.strip()]
    return names



def main():
    """Set up a Game instance and start the main loop."""
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
