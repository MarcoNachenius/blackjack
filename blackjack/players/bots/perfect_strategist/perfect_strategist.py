from blackjack.players.player_abc import Player
from blackjack.game_objects.hand import Hand
from blackjack.game_objects.card import Card
from blackjack.strategy_manager.player_strategies.hard_totals import HardTotalStrategy
from blackjack.strategy_manager.player_strategies.soft_totals import SoftTotalStrategy
import blackjack.players.bots.perfect_strategist.strategy_matrixes as strategy_matrixes

from typing import List

class PerfectStrategist(Player):
    """
    The perfect strategist never takes insurance when offered
    """
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
        self.hard_total_strategy = HardTotalStrategy(starting_matrix=strategy_matrixes.hard_totals)
        self.soft_total_strategy = SoftTotalStrategy(starting_matrix=strategy_matrixes.soft_totals)
        
    def request_split_pair(self, dealer_upcard: Card) -> bool:
        return False
    
    def request_bet_amount(self) -> int:
        return 10
    
    def request_hit(self, dealer_upcard: Card) -> bool:
        return False
    
    def request_double_down(self, dealer_upcard: Card, player_hand: Hand) -> bool:
        action_number: int = None
        # Check for hard total value
        if player_hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=player_hand.lowest_score())
        # Check if hand is pair
        elif player_hand.is_splittable():
            # TODO
            action_number = 0
        # Asssumes player has non-pair hand containing at least one ace
        else: 
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=player_hand.lowest_score())
        
        # Check for double down action number
        if action_number and (action_number == 2 or action_number == 3):
            return True
        # Assumes action number instructs player do reject double down offer
        return False
    
    def request_insurance(self) -> bool:
        return False