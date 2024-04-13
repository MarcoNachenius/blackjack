from abc import ABC
from typing import List
import numpy as np
class StrategyMatrix(ABC):
    """
    Player strategies are two-dimensional arrays. Their width(x-axis point) represents a point value of the dealer's up-card. 
    Their height(y-axis point) represents the value of the player hand.  
    """
    
    # Key = Point value of dealer up-card
    # Value = x-axis index number of 2d array
    UPCARD_POINTS_TO_INDEX_NUMBER: dict[int, int] = {
        1 : 9, # Ace
        2 : 0,
        3 : 1,
        4 : 2,
        5 : 3,
        6 : 4,
        7 : 5,
        8 : 6,
        9 : 7,
        10 : 8 # Jack, Queen, King
    }
    
    def __init__(self, width: int, height: int, starting_matrix: np.ndarray = None) -> None:
        self.strategy_matrix = np.zeros(shape=(height, width), dtype=int)
        if starting_matrix is not None:
            self.set_strategy_matrix(starting_matrix)
    
    def get_strategy_matrix(self) -> np.ndarray:
        """Getter method for strategy_matrix."""
        return self.strategy_matrix

    def set_strategy_matrix(self, matrix: np.ndarray) -> None:
        """
        Setter method for strategy_matrix.

        Args:
            matrix (np.ndarray): The new strategy matrix to set.
        """
        if isinstance(matrix, np.ndarray):
            self.strategy_matrix = matrix
        else:
            raise TypeError("Strategy matrix must be a numpy array.")
    
    def get_coordinate(self, x_coordinate: int, y_coordinate: int) -> int:
        """
        Returns value of 2d strategy matrix based on provided x and y coordinates.
        
        For example, suppose self.strategy_matrix is set to the following 3x4 array:
        ([1, 2, 3], [4, 5, 6], [9, 9, 9], [2, 7, 8])
        
        The 2d matrix's x-y point values look like this:
        
                      (Y-coordinate) 
                             |
                             v      
        (X-coordinate) ->      (0)(1)(2) 
                            (0)[1, 2, 3]
                            (1)[4, 5, 6]
                            (2)[9, 9, 9]
                            (3)[2, 7, 8]
            
        Return values will look like this:
        self.get_coordinate(0, 0) -> 1 
        self.get_coordinate(2, 2) -> 9
        self.get_coordinate(1, 3) -> 7
        """
        return self.get_strategy_matrix()[y_coordinate][x_coordinate]
    
    def set_coordinate(self, x_coordinate: int, y_coordinate: int, value: int):
        """
        Sets value of 2d strategy matrix based on provided x and y coordinates.\n
        """
        self.get_strategy_matrix()[y_coordinate][x_coordinate] = value
    
