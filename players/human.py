from players.player import Player
from card import Card
from hand import Hand
import constants

from typing import List

class Human(Player):
    """docstring for Human."""
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
    
    def request_split_pair(self) -> bool:
        response = input("Split pair? [y/n]")
        if response == "y":
            return True
    
    def request_round_participation(self) -> bool:
        # Exeptions
        # Does player have enough chips to bet?
        participation_request = input("Would you like to play the next round? [y/n]")
        if participation_request == "y":
            return True
        else:
            return False
    
    def request_bet_amount(self) -> int:
        # Exceptions
        # Is player placing a valid bet? (Not enough or too much)
        total_bet_amount = int(input("Enter the amount of chips you would like to bet"))
        return total_bet_amount
    
    def request_hit(self, split_hand=False) -> bool:
        hitme_request = input("Would you like to add card to hand? [y/n]")
        if hitme_request == "y":
            return True
        return False
    
    def request_double_down(self, dealer_card: Card):
        pass
    
    def request_insurance(self) -> bool:
        insurance_request = input("Would you like to buy insurance? [y/n]")
        if insurance_request == "y":
            return True
        # Returns false for any other value than "y"
        return False
