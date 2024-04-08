import unittest
from blackjack.strategy_manager.player_strategies.strategy_abc import StrategyMatrix
import numpy as np

class test_strategy_matrix(unittest.TestCase):
    
    def test_get_and_set_strategy_matrix(self):
        matrix = np.array([[1, 2], [3, 4]])
        obj = StrategyMatrix(2, 2)
        obj.set_strategy_matrix(matrix)
        self.assertEqual(obj.get_strategy_matrix().all(), np.array([[1, 2], [3, 4]]).all())
