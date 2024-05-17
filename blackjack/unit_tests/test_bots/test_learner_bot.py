import unittest
import numpy as np
from blackjack.strategy_manager.learning_bot_matrixes.learning_bot_strategies import LbStrategy

class TestStrategyMatrixes(unittest.TestCase):

    def setUp(self):
        self.width = 10
        self.height = 18
        self.depth = 7
        self.strategy_matrix = LbStrategy(width=self.width, height=self.height, depth=self.depth)
        self.matrix = self.strategy_matrix.get_strategy_matrix()
        self.expected_shape = (self.height, self.width, self.depth, 2)

    def test_matrix_shape(self):
        self.assertEqual(self.matrix.shape, self.expected_shape, f"Expected shape {self.expected_shape}, but got {self.matrix.shape}")

    def test_matrix_is_numpy_array(self):
        self.assertIsInstance(self.matrix, np.ndarray, "Strategy matrix is not a numpy array")

    def test_matrix_dtype(self):
        self.assertEqual(self.matrix.dtype, int, f"Expected dtype int, but got {self.matrix.dtype}")

    def test_matrix_list_usage(self):
        self.assertEqual(len(self.matrix), self.height)
        self.assertEqual(len(self.matrix[0]), self.width)
        self.assertEqual(len(self.matrix[0][0]), self.depth)
        self.assertEqual(len(self.matrix[0][0][0]), 2)
    
    def test_update_values(self):
        # Test the update_values method
        y_coordinate = 5
        x_coordinate = 3
        z_coordinate = 2
        trials = 10
        points = 20

        # Update the values in the strategy matrix
        self.strategy_matrix.update_values(y_coordinate, x_coordinate, z_coordinate, trials, points)

        # Assert the values are updated correctly
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 0], trials,
                        f"Expected trials value {trials}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 0]}")
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 1], points,
                        f"Expected points value {points}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 1]}")

    def test_update_values_multiple(self):
        # Test multiple updates
        updates = [
            (0, 0, 0, 1, 2),
            (17, 9, 6, 15, 30),
            (10, 5, 3, 25, 50)
        ]

        for y, x, z, trials, points in updates:
            self.strategy_matrix.update_values(y, x, z, trials, points)
            self.assertEqual(self.matrix[y, x, z, 0], trials,
                            f"Expected trials value {trials} at ({y}, {x}, {z}), but got {self.matrix[y, x, z, 0]}")
            self.assertEqual(self.matrix[y, x, z, 1], points,
                            f"Expected points value {points} at ({y}, {x}, {z}), but got {self.matrix[y, x, z, 1]}")
    
    def test_award_win(self):
        # Test the award_win method
        y_coordinate = 5
        x_coordinate = 3
        z_coordinate = 2

        # Get initial values
        initial_trials = self.matrix[y_coordinate, x_coordinate, z_coordinate, 0]
        initial_points = self.matrix[y_coordinate, x_coordinate, z_coordinate, 1]

        # Award a win
        self.strategy_matrix.award_win(y_coordinate, x_coordinate, z_coordinate)

        # Assert the values are updated correctly
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 0], initial_trials + 1,
                         f"Expected trials value {initial_trials + 1}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 0]}")
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 1], initial_points + 2,
                         f"Expected points value {initial_points + 2}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 1]}")

    def test_award_draw(self):
        # Test the award_draw method
        y_coordinate = 5
        x_coordinate = 3
        z_coordinate = 2

        # Get initial values
        initial_trials = self.matrix[y_coordinate, x_coordinate, z_coordinate, 0]
        initial_points = self.matrix[y_coordinate, x_coordinate, z_coordinate, 1]

        # Award a draw
        self.strategy_matrix.award_draw(y_coordinate, x_coordinate, z_coordinate)

        # Assert the values are updated correctly
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 0], initial_trials + 1,
                        f"Expected trials value {initial_trials + 1}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 0]}")
        self.assertEqual(self.matrix[y_coordinate, x_coordinate, z_coordinate, 1], initial_points + 1,
                        f"Expected points value {initial_points + 1}, but got {self.matrix[y_coordinate, x_coordinate, z_coordinate, 1]}")

if __name__ == '__main__':
    unittest.main()