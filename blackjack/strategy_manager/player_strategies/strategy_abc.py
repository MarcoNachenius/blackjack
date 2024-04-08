from abc import ABC
import numpy as np
class StrategyMatrix(ABC):
    """
    Player strategies are two-dimensional arrays. The x-axis represents the value of the dealer up-card. 
    The y-axis represents the value of the player hand.  
    """
    def __init__(self, width: int = 0, height: int = 0) -> None:
        self.strategy_matrix = np.zeros(shape=(width, height), dtype=int)
    
    def find_action(x_value: int, y_value: int) -> int:
        """
        Returns the value of the strategy matrix based on provided x and y axis values.\n
        \n
        For example, suppose strategy is the following 3x4 np array:\n
        ([1, 2, 3], [4, 5, 6], [9, 9, 9], [20, 7, 8])
        \n
        Return values will be the following:\n
        self.find_action(0,0) -> 1 \n
        self.find_action(2,2) -> 9\n
        self.find_action(3,1) -> 7\n
        """
    def get_strategy_matrix(self) -> np.ndarray:
        """Getter method for strategy_matrix."""
        return self._strategy_matrix

    def set_strategy_matrix(self, value: np.ndarray) -> None:
        """
        Setter method for strategy_matrix.

        Args:
            value (np.ndarray): The new strategy matrix to set.
        """
        if isinstance(value, np.ndarray):
            self._strategy_matrix = value
        else:
            raise TypeError("Strategy matrix must be a numpy array.")

