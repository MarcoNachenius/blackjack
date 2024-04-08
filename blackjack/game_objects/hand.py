from blackjack.game_objects.card import Card

from typing import List

class Hand(object):
    """Only first_card or starting_hand may be used as """
    def __init__(self, first_card: Card = None, starting_hand: List[Card] = None):
        """first_card and starting_hand may not be given values simultaneously"""
        self.hand_id: int = 0
        self.cards: List[Card] = starting_hand or []
        if first_card:
            self.cards.append(first_card)
        self.active: bool = True
        self.doubled_down: bool = False
        self.bust: bool = False
        self.rejected_split_request: bool = False
        self.amount_betted: int = 0
        self.final_outcome: str = ""
    
    def reject_split_request(self):
        """
        Enables status of hand to indicate that split request was received and rejected
        """
        self.set_rejected_split_request(True)
    
    def add_card (self, card: Card):
        new_card_list = self.get_cards()
        new_card_list.append(card)
        self.set_cards(new_card_list)
        return
       
    def deactivate(self):
        """
        Changes active status(self.active) of hand
        """
        self.active = False
        return
    
    def is_splittable(self) -> bool:
        """
        Returns True if first two cards of player hand are a pair
        """
        # Hand must have two cards in order to be split
        if len(self.get_cards()) != 2:
            return False
        if self.get_cards()[0].rank != self.get_cards()[1].rank:
            return False
        if self.get_rejected_split_request():
            return False
        return True
    
    def full_names_list(self) -> List[str]:
        """
        Returns a list of the full names of every card in a hand. \n
        Example:\n
        ["Ace of Spades", "Queen of Hearts"]
        """
        full_names_list = []
        for card in self.get_cards():
            full_names_list.append(card.full_name())
        return full_names_list
        
        
    def has_natural_blackjack(self) -> bool:
        """
        Checks the first two cards of a hand for a natural blackjack. 
        Returns True if one card is an Ace and the other is a 10-point card
        """
        # Check if hand is appropriate size
        if len(self.get_cards()) != 2:
            return False
        # Check for presence of 10 point card and ace
        found_ace_card = False
        found_ten_point_card = False
        # Check for aces
        if self.get_cards()[0].rank == "Ace":
            found_ace_card = True
        # Check for 10-point card
        if self.get_cards()[1].points == 10:
            found_ten_point_card = True
        return found_ace_card and found_ten_point_card
    
    def is_busted(self) -> bool:
        """
        Returns true if player hand is bust
        """
        return self.lowest_score() > 21
        
    def lowest_score(self) -> int:
        """
        Returns point amount for hand where all Aces are given 1 point
        """
        return sum(card.points for card in self.cards)
    
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
        Returns the highest possible point count of a hand without it being bust.\n
        Returns 0 if hand is bust
        """
        # Check if lowest point count is over 21
        if self.lowest_score() > 21:
            return 0
        # Check for Aces in hand
        if self.amount_of_aces == 0:
            return self.lowest_score()
        # Check for blackjack
        if self.highest_score() == 21:
            return self.highest_score()
        # Calculate highest non-bust amount if hand has multiple Aces
        multi_ace_score = self.lowest_score()
        if self.amount_of_aces() > 0 and multi_ace_score < 12:
            return multi_ace_score + 10
        return multi_ace_score 
    
    def amount_of_aces(self) -> int:
        """
        Returns the number of aces in a hand
        """
        return sum(1 for card in self.cards if card.rank == "Ace")
    
    
    # Getter for cards
    def get_cards(self) -> List[Card]:
        return self.cards

    # Setter for cards
    def set_cards(self, cards: List[Card]):
        if not isinstance(cards, list) or not all(isinstance(card, Card) for card in cards):
            raise ValueError("cards must be a list of Card instances")
        self.cards = cards

    # Getter for active
    def is_active(self) -> bool:
        return self.active

    # Setter for active
    def set_active(self, active: bool):
        if not isinstance(active, bool):
            raise ValueError("active must be a boolean value")
        self.active = active

    # Getter for doubled_down
    def is_doubled_down(self) -> bool:
        return self.doubled_down

    # Setter for doubled_down
    def set_doubled_down(self, doubled_down: bool):
        if not isinstance(doubled_down, bool):
            raise ValueError("doubled_down must be a boolean value")
        self.doubled_down = doubled_down

    # Getter for bust
    def is_bust(self) -> bool:
        return self.bust

    # Setter for bust
    def set_bust(self, bust: bool):
        if not isinstance(bust, bool):
            raise ValueError("bust must be a boolean value")
        self.bust = bust
    
    # Getter for rejected_split_request
    def get_rejected_split_request(self) -> bool:
        return self.rejected_split_request

    # Setter for rejected_split_request
    def set_rejected_split_request(self, rejected_split_request: bool):
        if not isinstance(rejected_split_request, bool):
            raise ValueError("rejected_split_request must be a boolean value")
        self.rejected_split_request = rejected_split_request
    
    # Getter for amount_betted
    def get_amount_betted(self) -> int:
        return self.amount_betted
    
    # Setter for amount_betted
    def set_amount_betted(self, amount_betted: int):
        if not isinstance(amount_betted, int):
            raise ValueError("amount_betted must be an int value")
        self.amount_betted = amount_betted
    
    def current_bet_amount(self) -> int:
        """
        Returns the amount of chips that are betted for
        a hand, adjusting when doubled down. 
        """
        current_bet_amount = self.get_amount_betted()
        if self.is_doubled_down():
            current_bet_amount *= 2
        return current_bet_amount
    
    # Getter for final_outcome
    def get_final_outcome(self) -> str:
        return self.final_outcome

    # Setter for final_outcome
    def set_final_outcome(self, final_outcome: str):
        if not isinstance(final_outcome, str):
            raise ValueError("final_outcome must be a string")
        self.final_outcome = final_outcome
    
    # Getter for hand_id
    def get_hand_id(self) -> int:
        return self.hand_id

    # Setter for hand_id
    def set_hand_id(self, hand_id: int):
        if not isinstance(hand_id, int):
            raise ValueError("hand_id must be a int")
        self.hand_id = hand_id