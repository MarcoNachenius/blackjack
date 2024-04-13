import unittest
from blackjack.strategy_manager.player_strategies.strategy_abc import StrategyMatrix
import numpy as np

class test_strategy_matrix(unittest.TestCase):
    
    def test_get_and_set_strategy_matrix(self):
        matrix = np.array([[1, 2], [3, 4]])
        strategy_matrix = StrategyMatrix(2, 2)
        strategy_matrix.set_strategy_matrix(matrix)
        self.assertEqual(strategy_matrix.get_strategy_matrix().all(), np.array([[1, 2], [3, 4]]).all())
    
    def test_get_and_set_coordinates(self):
        matrix = np.array([ [1, 2, 3], [4, 5, 6], [9, 9, 9], [2, 7, 8] ])
        strategy_matrix = StrategyMatrix(3, 4)
        self.assertEqual(strategy_matrix.get_coordinate(1, 3), 0)
        # Set coordinate point to 5
        strategy_matrix.set_coordinate(1, 3, 5)
        self.assertEqual(strategy_matrix.get_coordinate(1, 3), 5)
        strategy_matrix.set_strategy_matrix(matrix)
        self.assertEqual(strategy_matrix.get_coordinate(0, 0), 1)
        self.assertEqual(strategy_matrix.get_coordinate(2, 2), 9)
        self.assertEqual(strategy_matrix.get_coordinate(1, 3), 7)
