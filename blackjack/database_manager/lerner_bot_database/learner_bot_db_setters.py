import sqlite3

from blackjack.database_manager.strategy_database.strategy_db_setters import StrategyDbSetters
from blackjack.strategy_manager.learning_bot_matrixes.learning_bot_strategies import LbStrategy

class LearningBotDbSetters(StrategyDbSetters):
    
    @classmethod
    def increase_hard_totals_memory_trials_and_points(cls, db_path: str, hard_total_memory_strategy: LbStrategy):
        """
        Increases Trials and Points column values of the HardTotalsMemory table with trials and points
        amounts of the provided hard total memory matrix.
        """
        # Establish db connection
        connection = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        # Create iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(18))
        z_coordinate_index_range = list(range(8))
        
        # Iterate through entire LbStrategy matrix
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Retrieve trials and points numbers
                    trials_and_points_list = hard_total_memory_strategy.get_strategy_matrix()[y_coordinate][x_coordinate][z_coordinate]
                    trials = trials_and_points_list[0]
                    points = trials_and_points_list[1]
                    
                    # Skip iteration if there are 0 trials
                    if trials == 0:
                        continue
                    
                    # Create rest of db column values
                    player_score = cls.HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[y_coordinate]
                    dealer_upcard_points = x_coordinate + 1
                    action_number = z_coordinate
                    
                    # Create sql command that will be sent to the database
                    update_values_sql_command = '''UPDATE HardTotalsMemory SET
                                                    Trials = Trials + ?,
                                                    OutcomeScore = OutcomeScore + ?
                                                    WHERE
                                                    PlayerScore = ? AND
                                                    DealerUpcardPoints = ? AND
                                                    ActionNumber = ?'''

                    # Execute the update command with parameterized values
                    cursor.execute(update_values_sql_command, (int(trials), int(points), player_score, dealer_upcard_points, action_number))

                    # Commit the transaction
                    connection.commit()
        
        # Close connection to database
        connection.close()
    
    @classmethod
    def increase_soft_totals_memory_trials_and_points(cls, db_path: str, soft_total_memory_strategy: LbStrategy):
        """
        Increases Trials and Points column values of the SoftTotalsMemory table with trials and points
        amounts of the provided hard total memory matrix.
        """
        # Establish db connection
        connection = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        # Create iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(20))
        z_coordinate_index_range = list(range(8))
        
        # Iterate through entire LbStrategy matrix
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Retrieve trials and points numbers
                    trials_and_points_list = soft_total_memory_strategy.get_strategy_matrix()[y_coordinate][x_coordinate][z_coordinate]
                    trials = trials_and_points_list[0]
                    points = trials_and_points_list[1]
                    
                    # Skip iteration if there are 0 trials
                    if trials == 0:
                        continue
                    
                    # Create rest of db column values
                    player_score = cls.SOFT_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[y_coordinate]
                    dealer_upcard_points = x_coordinate + 1
                    action_number = z_coordinate
                    
                    # Create sql command that will be sent to the database
                    update_values_sql_command = '''UPDATE SoftTotalsMemory SET
                                                    Trials = Trials + ?,
                                                    OutcomeScore = OutcomeScore + ?
                                                    WHERE
                                                    PlayerScore = ? AND
                                                    DealerUpcardPoints = ? AND
                                                    ActionNumber = ?'''

                    # Execute the update command with parameterized values
                    cursor.execute(update_values_sql_command, (int(trials), int(points), player_score, dealer_upcard_points, action_number))

                    # Commit the transaction
                    connection.commit()
        
        # Close connection to database
        connection.close()
    
    @classmethod
    def increase_split_pairs_memory_trials_and_points(cls, db_path: str, split_pair_memory_strategy: LbStrategy):
        """
        Increases Trials and Points column values of the SplitPairsMemory table with trials and points
        amounts of the provided hard total memory matrix.
        """
        # Establish db connection
        connection = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        # Create iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(10))
        z_coordinate_index_range = list(range(2))
        
        # Iterate through entire LbStrategy matrix
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Retrieve trials and points numbers
                    trials_and_points_list = split_pair_memory_strategy.get_strategy_matrix()[y_coordinate][x_coordinate][z_coordinate]
                    trials = trials_and_points_list[0]
                    points = trials_and_points_list[1]
                    
                    # Skip iteration if there are 0 trials
                    if trials == 0:
                        continue
                    
                    # Create rest of db column values
                    player_score = cls.SPLIT_PAIR_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[y_coordinate]
                    dealer_upcard_points = x_coordinate + 1
                    action_number = z_coordinate
                    
                    # Create sql command that will be sent to the database
                    update_values_sql_command = '''UPDATE SplitPairsMemory SET
                                                    Trials = Trials + ?,
                                                    OutcomeScore = OutcomeScore + ?
                                                    WHERE
                                                    PlayerScore = ? AND
                                                    DealerUpcardPoints = ? AND
                                                    ActionNumber = ?'''

                    # Execute the update command with parameterized values
                    cursor.execute(update_values_sql_command, (int(trials), int(points), player_score, dealer_upcard_points, action_number))

                    # Commit the transaction
                    connection.commit()
        
        # Close connection to database
        connection.close()