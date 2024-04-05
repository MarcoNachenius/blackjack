from blackjack.hand import Hand
from blackjack import constants

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
    def __init__(self, player_name: str = "", custom_starting_hands: List[Hand] = None, custom_starting_chips: int = 0, custom_initial_bet_amount: int = 0):
        self.player_id: int = 0
        self.player_name = player_name # Required field
        self.hands: List[Hand] = custom_starting_hands or [Hand()]
        self.hand_combo_id: int = 0
        self.chips: int = custom_starting_chips or constants.STARTING_CHIPS
        self.initial_bet_amount = 0 or custom_initial_bet_amount
        self.total_bet_amount: int = 0
        self.is_insured: bool = False
        self.total_winnings: int = 0
    
    def has_enough_to_bet(self) -> bool:
        """
        Returns True if player has enough chips to 
        """
        return self.get_chips() > constants.MIN_BET_AMOUNT
    
    def add_chips(self, amount: int):
        self.set_chips(self.get_chips() + amount)
    
    def subtract_chips(self, amount: int):
        self.set_chips(self.get_chips() - amount)
    
    def current_bet_amount(self) -> int:
        bet_amount = self.get_initial_bet_amount()
        if self.get_is_insured():
            bet_amount = math.ceil(bet_amount * 1.5)
        return bet_amount
    
    def has_active_hands(self) -> bool:
        """
        Returns true if player has any active hands
        """
        return any(hand.active for hand in self.hands)
    
    def is_able_to_insure(self) -> bool:
        """
        Returns true if player has enough chips available to buy insurance.
        If insurance amount is not a whole number, it will be rounded up(ceiling) to the nearest int 
        """
        return self.chips > math.ceil(self.initial_bet_amount * 0.5)
    
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
        potential_bet_amount = self.get_initial_bet_amount()
        # Check if player has enough chips
        if potential_bet_amount > self.get_chips():
            return False
        return True 
    
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
    
    
    def total_round_bet_amount(self) -> int:
        """
        Returns the total number of chips that the player
        has bet for the current round. 
        
        Takes into account:
            - Insurance
            - Double downs
        """
    
    # ABSTRACT METHODS
    @abstractclassmethod
    def request_split_pair(self) -> bool:
        """
        Requests if a player wants to split pair after first card of dealer is shown.\n
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
    def request_hit(self, hand: Hand) -> bool:
        """
        Returns True if a player wants dealer to add card to hand
        """
    
    @abstractclassmethod
    def request_double_down(self, hand: Hand) -> bool:
        """
        Returns True if player decides to double down a hand
        """
    
    @abstractclassmethod
    def request_insurance(self) -> bool:
        """
        Player only receives insurance request it possess enough chips
        
        Player may choose money amount, provided it falls within insurance
        limit (usually 50% of bet).
        """
    
    # Getters and setters
    # Assuming the class has these attributes: player_name, hands, chips, initial_bet_amount, total_bet_amount, is_insured

    # Getter for player_name
    def get_player_name(self) -> str:
        return self.player_name

    # Setter for player_name with type verification
    def set_player_name(self, player_name: str):
        if not isinstance(player_name, str):
            raise ValueError("player_name must be a string")
        self.player_name = player_name
    
    # Getter for hand_combo_id
    def get_hand_combo_id(self) -> int:
        return self.hand_combo_id

    # Setter for hand_combo_id with type verification
    def set_hand_combo_id(self, hand_combo_id: int):
        if not isinstance(hand_combo_id, int):
            raise ValueError("hand_combo_id must be an int")
        self.hand_combo_id = hand_combo_id
    
    # Getter for hands
    def get_hands(self) -> List[Hand]:
        return self.hands

    # Setter for hands with type verification
    def set_hands(self, hands: List[Hand]):
        if not all(isinstance(hand, Hand) for hand in hands):
            raise ValueError("All items in hands must be of type Hand")
        self.hands = hands

    # Getter for chips
    def get_chips(self) -> int:
        return self.chips

    # Setter for chips with type verification
    def set_chips(self, chips: int):
        if not isinstance(chips, int):
            raise ValueError("chips must be an integer")
        self.chips = chips

    # Getter for initial_bet_amount
    def get_initial_bet_amount(self) -> int:
        return self.initial_bet_amount

    # Setter for initial_bet_amount with type verification
    def set_initial_bet_amount(self, initial_bet_amount: int):
        if not isinstance(initial_bet_amount, int):
            raise ValueError("initial_bet_amount must be an integer")
        self.initial_bet_amount = initial_bet_amount

    # Getter for total_bet_amount
    def get_total_bet_amount(self) -> int:
        return self.total_bet_amount

    # Setter for total_bet_amount with type verification
    def set_total_bet_amount(self, total_bet_amount: int):
        if not isinstance(total_bet_amount, int):
            raise ValueError("total_bet_amount must be an integer")
        self.total_bet_amount = total_bet_amount

    # Getter for is_insured
    def get_is_insured(self) -> bool:
        return self.is_insured

    # Setter for is_insured with type verification
    def set_is_insured(self, is_insured: bool):
        if not isinstance(is_insured, bool):
            raise ValueError("is_insured must be a boolean")
        self.is_insured = is_insured

    # Getter for total_winnings
    def get_total_winnings(self) -> int:
        return self.total_winnings

    # Setter for total_winnings with type verification
    def set_total_winnings(self, total_winnings: int):
        if not isinstance(total_winnings, int):
            raise ValueError("total_winnings must be an integer")
        self.total_winnings = total_winnings

    # Getter for player_id
    def get_player_id(self) -> int:
        return self.player_id

    # Setter for player_id with type verification
    def set_player_id(self, player_id: int):
        if not isinstance(player_id, int):
            raise ValueError("player_id must be an integer")
        self.player_id = player_id
        
    def add_to_total_winnings(self, amount: int):
        if not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        self.set_total_winnings(self.get_total_winnings() + amount)
    
    def subtract_from_total_winnings(self, amount: int):
        if not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        self.set_total_winnings(self.get_total_winnings() - amount)