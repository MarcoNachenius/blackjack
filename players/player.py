from card import Card
from hand import Hand
import constants

from typing import List
from abc import ABC, abstractclassmethod

class Player(ABC):
    """
    By default, an instance of Player will contain empty hands when created.
    
    Players only express interest in requests. Any resulting resulting additions or removals of\n
    cards from hands is performed by the Dealer.
    
    Only players control methods that subtract chips from their balance.
    """
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None):
        self.player_name = player_name # Required field
        self.hands: List[Hand] = custom_starting_hands or [Hand()]
        self.chips: int = custom_starting_chips or constants.STARTING_CHIPS
        # Round properties
        self.initial_bet_amount = 0
        self.total_bet_amount: int = 0
        self.is_insured: bool = False
    
    def current_bet_amount(self): 
        """
        If player is insured, halves the amount of chips that can be doubled/split 
        """
        if self.is_insured:
            return self.current_bet_amount / 2
        return self.initial_bet_amount
    
    def add_chips(self, amount: int):
        self.chips += amount
    
    def subtract_chips(self, amount: int):
        self.chips -= amount
    
    def has_active_hands(self) -> bool:
        """
        Returns true if player has any active hands
        """
        for hand in self.hands:
            if hand.active:
                return True
        return False
    
    def is_able_to_split(self) -> bool:
        """
        Returns True if:
            - Player has enough chips
            - Player has less than max allowed hands
        """
        # Check if player has less than max allowed hands
        if len(self.hands) == constants.MAX_HAND_LIMIT:
            return False
        
        # Determine bet amount
        potential_bet_amount = self.initial_bet_amount
        # Check for player insurance
        if self.is_insured:
            potential_bet_amount /= 2
        
        # Check if player has enough chips
        if potential_bet_amount < self.chips:
            return False
        
        return False
    
    def is_able_to_double_down(self) -> bool:
        """
        Returns True if:
            - Player has enough chips
        """
        # Determine bet amount
        potential_bet_amount = self.initial_bet_amount
        # Check for player insurance
        if self.is_insured:
            potential_bet_amount /= 2
        
        # Check if player has enough chips
        if potential_bet_amount < self.chips:
            return False
    
    def insure(self):
        """
        Changes insurance status of player to True.
        """
        self.is_insured = True
        
    
    @abstractclassmethod
    def request_split_pair(self) -> bool:
        """
        Requests if a player wants to split pair after first card of dealer is shown\n
        Returns True if the player has decided to split hand. \n
        Removes the second card from the player hand and places it into the players' split hand
        TODO\n
        """
        pass
    
    @abstractclassmethod
    def request_bet_amount(self) -> int:
        """
        Returns the amount of chips that a player would like to bet\n
        If a player sends invalid bet amount, it will be excluded from round participation
        
        If amount of 0 is returned, player will be rejected from active players list
        """
        pass
    
    @abstractclassmethod
    def request_hit(self) -> bool:
        """
        Returns True if a player wants dealer to add card to hand
        """
    
    @abstractclassmethod
    def request_double_down(self, dealer_card: Card):
        """
        Player only receives double down request on first round
        """
    
    @abstractclassmethod
    def request_insurance(self) -> bool:
        """
        Player only receives insurance request it possess enough chips
        
        Player may choose money amount, provided it falls within insurance
        limit (usually 50% of bet).
        """