import  numpy as np
from blackjack.strategy_manager.strategy_matrixes.strategy_abc import StrategyMatrix

class HardTotalStrategy(StrategyMatrix):
    """
    All hard total strategies have 10x18 matrixes.
    The matrix array list is ordered from the highest non-bust player score(21) 
    to the lowest possible hard total score(5)
    
    Array index:
    self.strategy_matrix[0] -> Strategy when hard total equals 21
    self.strategy_matrix[17] -> Strategy when hard total equals 4
    
    Array values:
    0 = Stand
    1 = Hit
    2 = Double down if allowed, otherwise hit
    3 = Double down if allowed, otherwise stand 
    """
    
    PLAYER_SCORE_TO_INDEX ={
        21 : 0,
        20 : 1,
        19 : 2,
        18 : 3,
        17 : 4,
        16 : 5,
        15 : 6,
        14 : 7,
        13 : 8,
        12 : 9,
        11 : 10,
        10 : 11,
        9 : 12,
        8 : 13,
        7 : 14,
        6 : 15,
        5 : 16,
        4 : 17
    }
    
    def __init__(self, starting_matrix: np.ndarray = None) -> None:
        super().__init__(width=10, height=18, starting_matrix=starting_matrix)
    
    def get_action_number(self, dealer_upcard_points: int, player_hard_total: int) -> int:
        """
        Returns a numerical value that represents an action that the player should make.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand 
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[player_hard_total]
        return self.get_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate)
    
    def set_action_number(self, dealer_upcard_points: int, player_hard_total: int, new_action_number: int):
        """
        Sets a numerical value that represents an action that the player should make.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand 
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[player_hard_total]
        self.set_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate, value=new_action_number)
        return
    
        
        