import random
import  numpy as np
import math
from blackjack.strategy_manager.strategy_matrixes.strategy_abc import StrategyMatrix

class SoftTotalStrategy(StrategyMatrix):
    """
    All soft total strategies have 10x20 matrixes.
    The matrix array list is ordered from the highest non-bust player score(21) 
    to the lowest possible soft total score(3)
    
    Array index:
    self.strategy_matrix[0] -> Strategy when soft total equals 21
    self.strategy_matrix[19] -> Strategy when soft total equals 2
    
    Array values:
    0 = Stand
    1 = Hit
    2 = Double down if allowed, otherwise hit
    3 = Double down if allowed, otherwise stand
    4 = Insurance, hit
    5 = Insurance, stand
    6 = Insurance, double down, hit
    7 = Insurance, double down, stand 
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
        4 : 17,
        3 : 18,
        2 : 19
    }
    
    
    def __init__(self, starting_matrix: np.ndarray = None) -> None:
        super().__init__(width=10, height=20, starting_matrix=starting_matrix)
    
    def get_action_number(self, dealer_upcard_points: int, player_soft_total: int) -> int:
        """
        Returns a numerical value that represents an action that the player should make.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand 
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[player_soft_total]
        return self.get_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate)
    
    def set_action_number(self, dealer_upcard_points: int, player_soft_total: int, new_action_number: int):
        """
        Sets a numerical value that represents an action that the player should make.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand 
        """
        x_coordinate = self.UPCARD_POINTS_TO_INDEX_NUMBER[dealer_upcard_points]
        y_coordinate = self.PLAYER_SCORE_TO_INDEX[player_soft_total]
        self.set_coordinate(x_coordinate=x_coordinate, y_coordinate=y_coordinate, value=new_action_number)
        return
    
    @classmethod
    def generate_next_permutation(cls, current_matrix: np.ndarray) -> np.ndarray:
        """
        Returns the next permutation of a given 10x20 soft total strategy matrix.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand 
        """
        next_permutation = current_matrix
        # Turn 2d matrix into single array
        flattened_matrix = next_permutation.flatten()

        for i in range(len(flattened_matrix) -1, -1, -1):
            if flattened_matrix[i] < 7:
                flattened_matrix[i] += 1
                break
            # Assumes i == 7
            flattened_matrix[i] = 0
        
        # Convert single array back into 2d matrix
        for i, action_number in enumerate(flattened_matrix):
            y_coordinate = math.floor(i/10)
            x_coordinate = i % 10
            next_permutation[y_coordinate][x_coordinate] = action_number
        
        return next_permutation
    
    @classmethod
    def generate_random_permutation(cls) -> np.ndarray:
        """
        Returns a random permutation of a 10x20 soft total strategy matrix.
        
        Action number values:
        0 = Stand
        1 = Hit
        2 = Double down if allowed, otherwise hit
        3 = Double down if allowed, otherwise stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand 
        """
        random_matrix = np.zeros(shape=(20, 10), dtype=int)
        for y_point in range(20):
            for x_point in range(10):
                random_matrix[y_point][x_point] = random.randrange(8)
        return random_matrix