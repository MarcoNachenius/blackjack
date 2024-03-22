from blackjack.players.player import Player
from blackjack.hand import Hand
from blackjack.card import Card

from typing import List

class BasicStrategist(Player):
    """
    The Noman is a very basic bot that follows the following strategy:
        - Any requests that are given will be rejected
        - Player will always place initial bet of 10 chips
    """
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
        
    def request_split_pair(self) -> bool:
        return False
    
    def request_bet_amount(self) -> int:
        return 10
    
    def request_hit(self) -> bool:
        return False
    
    def request_double_down(self, dealer_card: Card):
        return False
    
    def request_insurance(self) -> bool:
        return False