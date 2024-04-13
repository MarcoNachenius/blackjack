from typing import List
from blackjack.game_objects.card import Card

# Strategy objects
NAMES_TO_POINTS_DICT = {
    "Ace" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5,
    "Six" : 6,
    "Seven" : 7,
    "Eight" : 8,
    "Nine" : 9,
    "Ten" : 10,
    "Jack" : 10,
    "King" : 10,
    "Queen" : 10 }

# Card objects
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
    "Queen" ]

# Shoe variables
PENETRATION_POINT_PERCENTAGE = 60


# Game Settings
ENABLE_INSURANCE = True
MAX_HAND_LIMIT = 4
MIN_BET_AMOUNT = 2
DEALER_HIT_LIMIT = 17
STARTING_CHIPS = 1000
DECKS_IN_PLAY = 5

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
