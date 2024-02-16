from typing import List
from card import Card

SUIT_TYPES = ["Spades", "Hearts", "Diamonds", "Clubs"]
CARD_NAMES = [
    "Ace",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "King",
    "Queen"]
DECKS_IN_PLAY = 5
STARTING_CHIPS = 1000

# Insurance
ENABLE_INSURANCE = True
INSURANCE_PAYBACK_PERCENTAGE: 200

# Unassigned
FIST_BLACKJACK_PAYBACK_PERCENTAGE = 150
MAX_HAND_LIMIT = 4


class Deck(object):
    """
    Deck doc string
    """
    @classmethod
    def full_deck(cls) -> List[Card]:
        """
        Returns a full deck of cards as a List. \n
        Aces are given a point value of 1 by default.
        """
        full_deck = []
        for suit in SUIT_TYPES:
            for i, rank in enumerate(CARD_NAMES):
                # Assign point values of 10 for Ten, Jack, Queen and King cards
                if i < 9: 
                    full_deck.append(Card(rank=rank, suit=suit, points=i+1))
                    continue
                full_deck.append(Card(rank=rank, suit=suit, points=10))
        return full_deck
    
    @classmethod
    def starting_deck(cls) -> List[Card]:
        """
        Returns a lost of all the cards that are on the table at the beginning of the game.
        """
        return [card for _ in range(DECKS_IN_PLAY) for card in Deck.full_deck()]
