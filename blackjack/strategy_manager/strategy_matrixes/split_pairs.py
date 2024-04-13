import  numpy as np
from blackjack.strategy_manager.strategy_matrixes.strategy_abc import StrategyMatrix

class SplitPairStrategy(StrategyMatrix):
    """
    All hard total strategies have 10x10 matrixes.
    The matrix array list is ordered from double Aces to double Twos. 
    
    For example, the perfect_strategist player's split matrix looks like this:
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #Aces
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Tens
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0] #Nines
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #Eights
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] #Sevens
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0] #Sixes
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Fives
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0] #Fours
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] #Threes
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] #Twos
    
    Array index:
    self.strategy_matrix[0] -> Strategy when player has a pair of Aces
    self.strategy_matrix[9] -> Strategy when player has a pair of Twos
    
    Array values:
    0 = Reject split request
    1 = Accept split request
    """
    
    PLAYER_SCORE_TO_INDEX ={
        2 : 0,
        20 : 1,
        18 : 2,
        16 : 3,
        14 : 4,
        12 : 5,
        10 : 6,
        8 : 7,
        6 : 8,
        4 : 9
    }
    
    def __init__(self, starting_matrix: np.ndarray = None) -> None:
        super().__init__(width=10, height=10, starting_matrix=starting_matrix)
    
    def get_action_number(self, dealer_upcard_points: int, split_pair_score: int) -> int:
        """
        Returns a numerical value that represents an action that the player should make.
        
        # SPLIT PAIR
        # 0 = Reject split request
        # 1 = Accept split request
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[split_pair_score]
        return self.get_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate)
    
    def set_action_number(self, dealer_upcard_points: int, split_pair_score: int, new_action_number: int):
        """
        Sets a numerical value that represents an action that the player should make.
        
        # SPLIT PAIR
        # 0 = Reject split request
        # 1 = Accept split request
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[split_pair_score]
        self.set_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate, value=new_action_number)
        return
    
        
        