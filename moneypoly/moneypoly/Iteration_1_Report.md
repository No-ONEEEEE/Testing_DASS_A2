# Iteration 1 Report – Pylint-Driven Cleanup (New Baseline)

## Scope

This iteration starts from the freshly restored original MoneyPoly code. The goal was to address the most straightforward pylint issues (missing documentation, unused imports, obvious style problems, and clearly incorrect or unsafe logic) while keeping structural design changes minimal.

## Pylint Command

- Command run from the game directory:
  - `python -m pylint main.py moneypoly/*.py --reports=n --score=n > pylint_output_new.txt`
- Output file for this iteration:
  - `pylint_output_new.txt`

## Key Changes in This Iteration

- **Documentation and Style**
  - Added module docstrings to:
    - `main.py`
    - `moneypoly/bank.py`
    - `moneypoly/board.py`
    - `moneypoly/cards.py`
    - `moneypoly/config.py`
    - `moneypoly/dice.py`
    - `moneypoly/game.py`
    - `moneypoly/player.py`
    - `moneypoly/property.py`
    - `moneypoly/ui.py`
  - Added or clarified function/class docstrings where pylint reported missing documentation.
  - Removed unused imports (e.g., `math` in `bank.py`, `sys` in `player.py`, `GO_TO_JAIL_POSITION` in `game.py`), and simplified simple boolean checks.

- **Card Definitions and Deck Logic (`moneypoly/cards.py`)**
  - Rewrapped long Chance and Community Chest card definitions to satisfy `C0301 (line-too-long)` without changing semantics.
  - Introduced a clean `CardDeck` class with methods `draw`, `peek`, `reshuffle`, and `cards_remaining`, and ensured it is used by the game engine.
  - Exposed the card collections as:
    - `CHANCE_CARDS`
    - `COMMUNITY_CHEST_CARDS`
  - Ensured there are no syntax errors and that pylint can successfully import `moneypoly.cards`.

- **Bank Logic (`moneypoly/bank.py`)**
  - Updated `collect` to *ignore non-positive amounts*, matching the comment and preventing negative collections from corrupting the bank's totals.
  - Updated `give_loan` to:
    - Ignore non-positive loan requests.
    - Check bank funds before issuing a loan and raise a clear `ValueError` if funds are insufficient.
    - Decrease the bank's internal funds when a loan is issued.

- **Player Logic (`moneypoly/player.py`)**
  - Improved `net_worth` so it now includes the value of owned properties (balance + sum of property prices).
  - Updated `move` to pay the Go salary when the player **passes or lands on** Go, not only on an exact landing, by tracking the old position.

- **Property Logic (`moneypoly/property.py`)**
  - Simplified `unmortgage` to avoid an unnecessary `else` after `return`, per pylint suggestion.
  - Fixed `PropertyGroup.all_owned_by` so it only returns `True` when **all** properties in the group are owned by the given player and the group is non-empty.

- **Game Flow (`moneypoly/game.py`)**
  - Fixed `find_winner` to select the player with **maximum** net worth instead of minimum.
  - Cleaned up the winner announcement to avoid a pointless f-string and to improve formatting.
  - Tidied several conditionals and loops (e.g., removing unnecessary parentheses after `not`, ensuring imports only include used names).
  - Ensured the module has a final newline and no syntax errors.

- **UI Helpers (`moneypoly/ui.py`)**
  - Reimplemented `safe_int_input` to catch `ValueError` explicitly and to correctly use the `default` parameter, removing the previous bare `except`.

## Pylint Status After Iteration 1

- The codebase is free of syntax errors under pylint.
- Most basic documentation, import, and simple style warnings are resolved.
- Remaining pylint messages are primarily **structural suggestions**, for example:
  - `R0902 too-many-instance-attributes` in core classes (`Game`, `Player`, `Property`).
  - `R0912 too-many-branches` in complex control-flow methods like the main game loop.
  - A minor recommendation to use an f-string in one formatted message and to simplify an `elif` after `break`.
- These remaining warnings reflect the inherent complexity of the game logic and would require more invasive refactoring; they are left as design trade-offs rather than quick fixes.

## Associated Commit

- Commit message: **`Iteration 1: Pylint docs, card deck, and logic cleanup`**
- This commit was pushed to the remote repository on branch `main`.

This report documents all the meaningful pylint-driven changes applied in Iteration 1 on the restored MoneyPoly codebase and serves as evidence for Section 1.2 of the assignment.
