from blackjack.players.player_abc import Player
from blackjack.game_objects.hand import Hand
from blackjack.game_objects.card import Card
# Strategy matrixes
from blackjack.strategy_manager.strategy_matrixes.hard_totals import HardTotalStrategy
from blackjack.strategy_manager.strategy_matrixes.soft_totals import SoftTotalStrategy
from blackjack.strategy_manager.strategy_matrixes.split_pairs import SplitPairStrategy


from typing import List

class Strategist(Player):
    """
    Strategist bots follow all instructions based on their provided strategy matrixes. 
    Strategists always bet same amount of chips.
    
    Strategies:
    - When to hit
    - When to stand
    - When to double down
    - When to split
    - When to take insurance
    """
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
        self.hard_total_strategy = HardTotalStrategy()
        self.soft_total_strategy = SoftTotalStrategy()
        self.split_pair_strategy = SplitPairStrategy()
        
        
    def request_split_pair(self, dealer_upcard: Card, hand: Hand) -> bool:
        accept_request = False
        action_number = self.split_pair_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, split_pair_score=hand.lowest_score())
        if action_number == 1:
            accept_request = True
        return accept_request
    
    def request_bet_amount(self) -> int:
        return 10
    
    def request_hit(self, dealer_upcard: Card, hand: Hand) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
        # Assumes player has hand containing at least one ace
        else: 
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
        
        # Check for hit
        if action_number == 1:
            return True
        # Check for double down, hit
        if action_number == 2:
            return True
        # Check for insurance, hit
        if action_number == 4:
            return True
        # Check for insurance, double down, hit
        if action_number == 6:
            return True
        # Assumes action number instructs player to stand
        return False
    
    def request_double_down(self, dealer_upcard: Card, hand: Hand) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
        # Assumes player has hand containing at least one ace
        else: 
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
        
        # Check double down, hit
        if action_number == 2:
            return True
        # Check double down, stand
        if action_number == 3:
            return True
        # Check insurance, double down, stand
        if action_number == 6:
            return True
        # Assumes action number instructs player do reject double down offer
        return False
    
    def request_insurance(self, hand: Hand, dealer_upcard: Card) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
        # Assumes player has hand containing at least one ace
        else: 
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
        
        # Check insurance, hit
        if action_number == 4:
            return True
        # Check insurance, stand
        if action_number == 5:
            return True
        # Check for insurance, double down, hit
        if action_number == 6:
            return True
        # Check for insurance, double down, stand
        if action_number == 7:
            return True
        # Assumes action number instructs player to stand
        return False