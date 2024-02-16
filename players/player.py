from card import Card
from hand import Hand
import constants

from typing import List
from abc import ABC, abstractclassmethod
import math

class Player(ABC):
    """
    By default, an instance of Player will contain empty hands when created.
    
    Players only express interest in requests. Any resulting resulting additions or removals of\n
    cards from hands is performed by the Dealer.
    
    Only players control methods that subtract chips from their balance.
    """
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = 0, custom_initial_bet_amount: int = 0):
        self.player_name = player_name # Required field
        self.hands: List[Hand] = custom_starting_hands or [Hand()]
        self.chips: int = custom_starting_chips or constants.STARTING_CHIPS
        # Round properties
        self.initial_bet_amount = 0 or custom_initial_bet_amount
        self.total_bet_amount: int = 0
        self.is_insured: bool = False
    
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
    
    def is_able_to_insure(self) -> bool:
        """
        Returns true if player has enough chips available to buy insurance.
        If insurance amount is not a whole number, it will be rounded up(ceiling) to the nearest int 
        """
        if self.chips > math.ceil(self.initial_bet_amount * 0.5):
            return True
        return False
    
    def is_able_to_split(self) -> bool:
        """
        Returns True if:
            - Player has not previously rejected split request
            - Player has enough chips
            - Player has less than max allowed hands
        """
        # Check for previous split request
        # Check if player has less than max allowed hands
        if len(self.hands) >= constants.MAX_HAND_LIMIT:
            return False
        
        # Check if player has enough chips
        if self.initial_bet_amount > self.chips:
            return False
        
        return True
    
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
        Subtracts 50%(ceiling) of initial bet from player chips
        Changes insurance status of player to True.
        """
        self.is_insured = True
        self.subtract_chips(math.ceil(self.initial_bet_amount * 0.5))
    
    def add_chips(self, amount: int):
        """
        Adds amount(int) to player chips
        """
        self.chips += amount
    
    def subtract_chips(self, amount: int):
        """
        Subtracts amount(int) from player chips
        """
        self.chips -= amount
    
    @abstractclassmethod
    def request_split_pair(self) -> bool:
        """
        Requests if a player wants to split pair after first card of dealer is shown\n
        Returns True if the player has decided to split hand. \n
        Removes the second card from the player hand and places it into the players' split hand
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