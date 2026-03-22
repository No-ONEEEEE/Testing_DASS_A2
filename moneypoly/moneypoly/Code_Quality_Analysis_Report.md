# Code Quality Analysis – MoneyPoly (Pylint-Driven Iterations)

## Overview

This report describes how pylint was used to iteratively improve the quality of the MoneyPoly codebase. The work was done in three iterations. Each iteration:

- Started from the previous commit.
- Used `pylint` to identify issues.
- Applied focused fixes (documentation, style, safety, or logic).
- Was recorded as a separate git commit and a short per-iteration report.

Pylint was always run from the game directory with:

```bash
python -m pylint main.py moneypoly/*.py --reports=n --score=n
```

The per-iteration reports are:

- Iteration 1: `Iteration_1_Report.md`
- Iteration 2: `Iteration_2_Report.md`
- Iteration 3: `Iteration_3_Report.md`

All three are in the same folder as this report.

---

## Iteration 1 – Documentation, Safety, and Core Logic Fixes

**Goals:**

- Eliminate basic pylint warnings (missing docstrings, unused imports, simple style problems).
- Fix clear logic and safety issues revealed by static analysis and white-box reasoning.

**Key Changes:**

1. **Docstrings and Style**
   - Added module and function/class docstrings across:
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
   - Removed unused imports and simplified boolean comparisons and other small style issues.

2. **Bank Logic (`bank.py`)**
   - `collect` now ignores non-positive amounts (matching its own comment and avoiding corrupting totals with negative values).
   - `give_loan` now:
     - Ignores non-positive loan requests.
     - Checks available funds and raises a clear `ValueError` if the bank cannot afford the loan.
     - Reduces the bank's internal funds when a loan is issued.

3. **Player Logic (`player.py`)**
   - `net_worth` now includes both cash balance and the prices of all owned properties.
   - `move` now correctly pays the Go salary when the player **passes or lands on** Go by tracking the previous position.

4. **Property Logic (`property.py`)**
   - `unmortgage` was simplified to avoid an unnecessary `else` after `return`, per pylint.
   - `PropertyGroup.all_owned_by` was corrected to return `True` only when **all** properties in the group are owned by the given player, and the group is non-empty.

5. **Game Logic (`game.py`)**
   - `find_winner` now selects the player with the **maximum** net worth (previously it used `min`).
   - Rent payments and winner messaging were cleaned up to ensure money actually flows to property owners and the final message is clear.
   - Imports were pruned (unused names removed) and small style issues fixed.

6. **Card Definitions (`cards.py`)**
   - Introduced a `CardDeck` class with `draw`, `peek`, `reshuffle`, and `cards_remaining` methods.
   - Defined card lists as `CHANCE_CARDS` and `COMMUNITY_CHEST_CARDS` and ensured they are imported correctly by the game engine.

7. **UI Helpers (`ui.py`)**
   - `safe_int_input` now explicitly catches `ValueError` and returns the provided `default`, removing the previous bare `except`.

**Result:**

- Pylint no longer reported syntax errors or basic documentation/import issues.
- Several real logic bugs were fixed (bank balances, winner selection, Go salary, net worth, group-ownership, etc.).
- Captured in git as: **`Iteration 1: Pylint docs, card deck, and logic cleanup`**.

---

## Iteration 2 – Polishing and Per-Iteration Reporting

**Goals:**

- Apply a small additional round of safe pylint-driven improvements.
- Introduce per-iteration reports and capture the state of remaining warnings.

**Key Changes:**

1. **Winner Message (`game.py`)**
   - Converted the final winner announcement to a clean f-string:
     - Now prints: `"{winner.name} wins with a net worth of ${winner.net_worth()}!"`.
   - This addressed pylint's `C0209` suggestion and improved readability.

2. **Card Deck File Tail (`cards.py`)**
   - Normalized the end of the file so `CardDeck.__repr__` is the last method and the file ends with a single newline.
   - This targeted the `C0305 trailing-newlines` warning (cosmetic).

3. **Reporting**
   - Added:
     - `Iteration_1_Report.md` – detailed summary of Iteration 1.
     - `Iteration_2_Report.md` – description of these additional tweaks and the pylint status afterward.

**Pylint After Iteration 2:**

- Remaining messages were mostly structural:
  - `too-many-instance-attributes` (`R0902`) in `Game`, `Player`, `Property`.
  - `too-many-branches` (`R0912`) in complex game logic.
  - `too-many-arguments` / `too-many-positional-arguments` (`R0913` / `R0917`) in the `Property` constructor.
  - Cosmetic `trailing-newlines` warnings.
- Captured in git as: **`Iteration 2: Winner message and pylint reports`**.

---

## Iteration 3 – Targeted Structural Refactor

**Goals:**

- Improve the structure of a particularly important control-flow method without changing game behaviour.
- Re-run pylint and document final remaining warnings.

**Key Changes:**

1. **Jail Turn Handling (`game.py`, `_handle_jail_turn`)**

- **Before:**
  - The method used multiple early returns to handle:
    - Using a "Get Out of Jail Free" card.
    - Voluntary payment of the jail fine.
  - The "do nothing" case incremented `jail_turns` and applied a mandatory fine after three turns.

- **After (Iteration 3):**
  - The "Get Out of Jail Free" branch still returns immediately after resolving the turn (unchanged).
  - The voluntary-fine vs. "do nothing" path is now expressed as a clearer `if`/`else`:
    - **If the player pays the fine:**
      - Bank collects `JAIL_FINE`.
      - Player leaves jail and `jail_turns` resets to 0.
      - Player rolls and moves immediately.
    - **Else (player declines to pay):**
      - `jail_turns` increments.
      - Once `jail_turns >= 3`, the player must pay the mandatory fine, leave jail, and then roll and move.
  - Overall behaviour is preserved, but the control flow is easier to understand and maintain.

2. **Iteration 3 Report**

- Added `Iteration_3_Report.md` to describe this refactor and clarify the final pylint status.

**Pylint After Iteration 3:**

- Only structural and cosmetic messages remain:
  - `C0305 trailing-newlines` in `cards.py` (platform/line-ending related, cosmetic only).
  - `R0902`, `R0912`, `R0913`, `R0917`, and `R1723` in `game.py`, `player.py`, and `property.py` – all relating to:
    - Number of attributes on core classes.
    - Number of branches in complex control-flow.
    - Number of arguments in the `Property` constructor.
    - A stylistic `no-else-break` recommendation.

- Addressing these would require larger refactorings (splitting classes, decomposing big methods, redesigning constructors) and would increase complexity and risk for limited benefit.

- Captured in git as: **`Iteration 3: Jail turn refactor and report`**.

---

## Final Summary and Justification

Across three iterations, the MoneyPoly codebase was progressively improved using pylint as a guide:

- All **simple, local, and clearly safe** issues were fixed:
  - Missing docstrings and unused imports.
  - Unsafe constructs like bare `except`.
  - Logic bugs in banking, movement, rent, group-ownership, and winner selection.
  - Clarity issues in user messages and card handling.

- The remaining pylint messages are almost entirely **structural suggestions**:
  - They recommend splitting core classes or methods and altering constructor signatures.
  - Implementing them would significantly change the design and potentially introduce new bugs, with little gain for this assignment.

Therefore:

- The current state represents a good balance between code quality and scope.
- Pylint has been used effectively to:
  - Detect genuine bugs and design problems.
  - Drive incremental, well-documented improvements.
  - Provide a clear record (via commits and iteration reports) of how the code was improved over time.
