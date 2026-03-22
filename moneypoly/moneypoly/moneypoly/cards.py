"""Definitions of Chance and Community Chest cards and their deck logic."""

import random


CHANCE_CARDS = [
    {
        "message": "Advance to Go (Collect $200)",
        "effect": lambda player, bank, board: player.move(0, board),
    },
    {
        "message": "Bank error in your favor – Collect $200",
        "effect": lambda player, bank, board: bank.give_loan(player, 200),
    },
    {
        "message": "Doctor's fees – Pay $50",
        "effect": lambda player, bank, board: bank.collect(player, 50),
    },
    {
        "message": "Get Out of Jail Free – This card may be kept until needed, or sold",
        "effect": lambda player, bank, board: player.get_out_of_jail_free_cards.append(
            "Chance"
        ),
    },
    {
        "message": "Go to Jail – Go directly to Jail, do not pass Go, do not collect $200",
        "effect": lambda player, bank, board: player.go_to_jail(board),
    },
    {
        "message": "It is your birthday – Collect $10 from every player",
        "effect": lambda player, bank, board: [
            bank.transfer_money(p, player, 10) for p in board.players if p != player
        ],
    },
    {
        "message": "Grand Opera Night – Collect $50 from every player for opening night seats",
        "effect": lambda player, bank, board: [
            bank.transfer_money(p, player, 50) for p in board.players if p != player
        ],
    },
    {
        "message": "Income Tax refund – Collect $20",
        "effect": lambda player, bank, board: bank.give_loan(player, 20),
    },
    {
        "message": "Life Insurance Matures – Collect $100",
        "effect": lambda player, bank, board: bank.give_loan(player, 100),
    },
    {
        "message": "Pay Hospital Fees of $100",
        "effect": lambda player, bank, board: bank.collect(player, 100),
    },
    {
        "message": "Pay School Fees of $50",
        "effect": lambda player, bank, board: bank.collect(player, 50),
    },
    {
        "message": "Receive $25 Consultancy Fee",
        "effect": lambda player, bank, board: bank.give_loan(player, 25),
    },
    {
        "message": "You are assessed for street repairs – $40 per house, $115 per hotel",
        "effect": lambda player, bank, board: bank.collect(
            player, 40 * player.houses + 115 * player.hotels
        ),
    },
    {
        "message": "You have won second prize in a beauty contest – Collect $10",
        "effect": lambda player, bank, board: bank.give_loan(player, 10),
    },
    {
        "message": "You inherit $100",
        "effect": lambda player, bank, board: bank.give_loan(player, 100),
    },
    {
        "message": "From sale of stock you get $50",
        "effect": lambda player, bank, board: bank.give_loan(player, 50),
    },
]

COMMUNITY_CHEST_CARDS = [
    {
        "message": "Advance to Go (Collect $200)",
        "effect": lambda player, bank, board: player.move(0, board),
    },
    {
        "message": "Bank error in your favor – Collect $200",
        "effect": lambda player, bank, board: bank.give_loan(player, 200),
    },
    {
        "message": "Doctor's fees – Pay $50",
        "effect": lambda player, bank, board: bank.collect(player, 50),
    },
    {
        "message": "Get Out of Jail Free – This card may be kept until needed, or sold",
        "effect": lambda player, bank, board: player.get_out_of_jail_free_cards.append(
            "Community Chest"
        ),
    },
    {
        "message": "Go to Jail – Go directly to Jail, do not pass Go, do not collect $200",
        "effect": lambda player, bank, board: player.go_to_jail(board),
    },
    {
        "message": "It is your birthday – Collect $10 from every player",
        "effect": lambda player, bank, board: [
            bank.transfer_money(p, player, 10) for p in board.players if p != player
        ],
    },
    {
        "message": "Grand Opera Night – Collect $50 from every player for opening night seats",
        "effect": lambda player, bank, board: [
            bank.transfer_money(p, player, 50) for p in board.players if p != player
        ],
    },
    {
        "message": "Income Tax refund – Collect $20",
        "effect": lambda player, bank, board: bank.give_loan(player, 20),
    },
    {
        "message": "Life Insurance Matures – Collect $100",
        "effect": lambda player, bank, board: bank.give_loan(player, 100),
    },
    {
        "message": "Pay Hospital Fees of $100",
        "effect": lambda player, bank, board: bank.collect(player, 100),
    },
    {
        "message": "Pay School Fees of $50",
        "effect": lambda player, bank, board: bank.collect(player, 50),
    },
    {
        "message": "Receive $25 Consultancy Fee",
        "effect": lambda player, bank, board: bank.give_loan(player, 25),
    },
    {
        "message": "You are assessed for street repairs – $40 per house, $115 per hotel",
        "effect": lambda player, bank, board: bank.collect(
            player, 40 * player.houses + 115 * player.hotels
        ),
    },
    {
        "message": "You have won second prize in a beauty contest – Collect $10",
        "effect": lambda player, bank, board: bank.give_loan(player, 10),
    },
    {
        "message": "You inherit $100",
        "effect": lambda player, bank, board: bank.give_loan(player, 100),
    },
    {
        "message": "From sale of stock you get $50",
        "effect": lambda player, bank, board: bank.give_loan(player, 50),
    },
]


class CardDeck:
    """Simple deck wrapper for Chance and Community Chest cards."""

    def __init__(self, cards):
        self.cards = list(cards)
        self.index = 0

    def draw(self):
        """Draw the next card, cycling back to the start when exhausted."""
        if not self.cards:
            return None
        card = self.cards[self.index % len(self.cards)]
        self.index += 1
        return card

    def peek(self):
        """Return the next card without advancing the index."""
        if not self.cards:
            return None
        return self.cards[self.index % len(self.cards)]

    def reshuffle(self):
        """Shuffle the deck and reset the draw index."""
        random.shuffle(self.cards)
        self.index = 0

    def cards_remaining(self):
        """Return how many cards remain before the deck cycles."""
        return len(self.cards) - (self.index % len(self.cards))

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"CardDeck({len(self.cards)} cards, next={self.index % len(self.cards)})"

