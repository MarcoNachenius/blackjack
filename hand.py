from card import Card

from typing import List

class Hand(object):
    """Only first_card or starting_hand may be used as """
    def __init__(self, first_card: Card = None, starting_hand: List[Card] = None):
        """first_card and starting_hand may not be given values simultaneously"""
        self.cards: List[Card] = starting_hand or []
        if first_card:
            self.cards.append(first_card)
        self.active: bool = True
        self.doubled_down = False
    
    def add_card(self, card: Card):
        """
        Adds card to hand(self.cards)
        """
        self.cards.append(card)
        
    def deactivate(self):
        """
        Changes active status(self.active) of hand
        """
        self.active = False
    
    def is_splittable(self) -> bool:
        """
        Returns True if first two cards of player hand are a pair
        """
        # Hand must have two cards in order to be split
        if len(self.cards) != 2:
            return False
        if self.cards[0].rank == self.cards[1].rank:
            return True
        return False
        
    def has_natural_blackjack(self) -> bool:
        """
        Checks the first two cards of a hand for a natural blackjack. 
        Returns True if one card is an Ace and the other is a 10-point card
        """
        ace_card = False
        ten_point_card = False
        for i in range(2):
            # Check for aces
            if self.cards[i].rank == "Ace":
                ace_card = True
            # Check for 10-point card
            if self.cards[i].points == 10:
                ten_point_card = True
        if ace_card and ten_point_card:
            return True
        return False