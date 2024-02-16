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
        self.doubled_down: bool = False
        self.bust: bool = False
        self.rejected_split_request: bool = False
    
    def reject_split_request(self):
        """
        Enables status of hand to indicate that split request was received and rejected
        """
        self.rejected_split_request = True
    
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
        if self.cards[0].rank != self.cards[1].rank:
            return False
        if self.rejected_split_request:
            return False
        return True
    
    def full_names_list(self) -> List[str]:
        """
        Returns a list of the full names of every card in a hand. \n
        Example:\n
        ["Ace of Spades", "Queen of Hearts"]
        """
        full_names_list = []
        for card in self.cards:
            full_names_list.append(card.full_name())
        return full_names_list
        
        
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
    
    def is_busted(self) -> bool:
        """
        Returns true if player hand is bust
        """
        return self.bust
        
    def lowest_score(self) -> int:
        """
        Returns point amount for hand where all Aces are given 1 point
        """
        score = 0
        for card in self.cards:
            score += card.points
        return score
    
    def highest_score(self) -> int:
        """
        Returns point amount for hand where all Aces are given 11 points
        """
        score = 0
        for card in self.cards:
            if card.rank == "Ace":
                score += 11
                continue
            score += card.points
        return score
    
    def set_busted(self):
        """
        Changes bust status of hand(self.bust) to True
        """
        self.bust = True
        
    def max_non_bust_score(self) -> int:
        """
        Returns the highest possible point count of a hand without it being bust.
        If the hand is bust, this method will return 0
        """
        # Check if hand is bust
        if self.is_busted():
            return 0
        # Check if lowest point count is over 21
        if self.lowest_score() > 21:
            return 0
        # Check for Aces in hand
        if self.amount_of_aces == 0:
            return self.lowest_score()
        # Check for natural blackjack
        if self.has_natural_blackjack():
            return 21
        # Check for regular blackjack
        if self.highest_score() < 22:
            return self.highest_score()
        
        # Calculate highest non-bust amount if hand has multiple Aces
        multi_ace_score = self.lowest_score()
        if self.amount_of_aces() > 0 and multi_ace_score + 10 < 22:
            return multi_ace_score + 10
        return multi_ace_score 
    
    def amount_of_aces(self) -> int:
        """
        Returns the number of aces in a hand
        """
        ace_count = 0
        for card in self.cards:
            if card.rank == "Ace":
                ace_count += 1
        if ace_count > 1:
            return True
        return False