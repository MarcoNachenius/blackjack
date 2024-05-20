import sqlite3
import numpy as np

from blackjack.database_manager.strategy_database.strategy_db_getters import StrategyDbGetters
from blackjack.database_manager.strategy_database.strategy_db_setters import StrategyDbSetters

class LearningBotDbGetters(StrategyDbGetters):
    
    @classmethod
    def get_next_hard_totals_matrix_to_test(cls, db_path : str) -> np.ndarray:
        """
        Returns a hard total strategy matrix from the learning bot simulation database
        that contains the actions numbers that need to be tested next.
        
        Matrix action numbers are retrieved by getting the last action number that was tested and increasing it by 1,
        or setting it to 0 if a higher action number does not exist.
        """
        # Create hard_total object that will be returned
        hard_total_matrix = np.zeros(dtype=int, shape=(18, 10))
        
        # Create iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(18))
        
        # Populate matrix values from database
        # Iterate through entire LbStrategy matrix
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                player_score = StrategyDbSetters.HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[y_coordinate]
                dealer_upcard_points = x_coordinate + 1
                hard_total_matrix[y_coordinate][x_coordinate] = cls.get_next_hard_totals_action_number_to_test(db_path=db_path, player_score=player_score, dealer_upcard_points=dealer_upcard_points)
        
        return hard_total_matrix
        
    @classmethod
    def get_next_hard_totals_action_number_to_test(cls, db_path: str, player_score: int, dealer_upcard_points) -> int:
        """
        Returns next action number that should be tested in a simulation.
        
        The action number is retrieved by getting the last action number that was tested and increasing it by 1,
        or setting it to 0 if a higher action number does not exist.
        """
        # Connect to database and create cursor
        connection = sqlite3.Connection(db_path)
        cursor = connection.cursor()

        # Select values from table
        select_action_numbers_list_sql_command = '''SELECT ActionNumber, Trials FROM HardTotalsMemory WHERE
                                                    PlayerScore = ? AND
                                                    DealerUpcardPoints = ?
                                                    ORDER BY ActionNumber'''
        # Execute SQL command and retrieve list
        query_rows = cursor.execute(select_action_numbers_list_sql_command, (player_score, dealer_upcard_points)).fetchall()
        connection.close()

        # Determine next action number to be tested
        action_number = query_rows[0][0]
        lowest_trials_number = query_rows[0][1]
        for row in query_rows:
            row_trials_amount = row[1]
            if row_trials_amount < lowest_trials_number:
                lowest_trials_number = row_trials_amount
                # Determine first action number with lowest trials values
                row_action_number = row[0]
                action_number = row_action_number

        return action_number