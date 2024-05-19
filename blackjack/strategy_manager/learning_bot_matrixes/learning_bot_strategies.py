import numpy as np 

class LbStrategy(object):
    '''
    ### Matrix Structure
    Strategy matrixes are three dimensional.
    
    ### How it works
    x_coordinate = dealer_upcard_points
    y_coordinate = player_hand_minimum_score
    z_coordinate = action_number
    strategy_matrix = LbStrategy(height = y_coordinate, width = x_coordinate, depth = z_coordinate)
    results_list = strategy_matrix[y_coordinate][x_coordinate][z_coordinate]
    amount_of_times_action_number_was_tried = results_list[0]
    points_gained_through_wins_and_draws = results_list[1]
    '''
    
    def __init__(self, height: int, depth: int, width = 10) -> None:
        self._strategy_matrix = np.zeros(dtype=int, shape=(height, width, depth, 2))
    
    def get_strategy_matrix(self):
        '''
        Returns the strategy matrix, which is a numpy array with shape (height, width, depth, 2).
        
        Returns:
            numpy.ndarray: The strategy matrix.
        '''
        return self._strategy_matrix

    def set_strategy_matrix(self, value):
        '''
        Sets the strategy matrix with the provided value if it is a numpy array with the correct shape.
        
        Args:
            value (numpy.ndarray): The new strategy matrix to set.
        
        Raises:
            ValueError: If the provided value is not a numpy array or does not have the correct shape.
        '''
        if isinstance(value, np.ndarray) and value.shape == self._strategy_matrix.shape:
            self._strategy_matrix = value
        else:
            raise ValueError(f"Provided value must be a numpy array with shape {self._strategy_matrix.shape}")
    
    def update_values(self, y_coordinate: int, x_coordinate: int, z_coordinate: int, trials: int, points: int):
        '''
        Updates the values at the specified coordinates in the strategy matrix.
        
        Args:
            y_coordinate (int): The player hand minimum score index number.
            x_coordinate (int): The dealer upcard points index number.
            z_coordinate (int): The action number index number.
            trials (int): The new amount of times action number was tried.
            points (int): The new points gained through wins and draws.
        '''
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 0] = trials
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 1] = points
    
    def award_win(self, y_coordinate: int, x_coordinate: int, z_coordinate: int):
        '''
        Awards a win by increasing trials by 1 and points by 1 at the specified coordinates in the strategy matrix.

        Args:
            y_coordinate (int): The player hand minimum score index number.
            x_coordinate (int): The dealer upcard points index number.
            z_coordinate (int): The action number index number.
        '''
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 0] += 1
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 1] += 1

    def award_loss(self, y_coordinate: int, x_coordinate: int, z_coordinate: int):
        '''
        Awards a loss by increasing trials by 1 and decrease points by 1 at the specified coordinates in the strategy matrix.

        Args:
            y_coordinate (int): The player hand minimum score index number.
            x_coordinate (int): The dealer upcard points index number.
            z_coordinate (int): The action number index number.
        '''
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 0] += 1
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 1] -= 1
    
    def award_draw(self, y_coordinate: int, x_coordinate: int, z_coordinate: int):
        '''
        Awards a draw by increasing trials by 1 at the specified coordinates in the strategy matrix.

        Args:
            y_coordinate (int): The player hand minimum score index number.
            x_coordinate (int): The dealer upcard points index number.
            z_coordinate (int): The action number index number.
        '''
        self._strategy_matrix[y_coordinate, x_coordinate, z_coordinate, 0] += 1