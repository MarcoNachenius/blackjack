import sqlite3
import numpy as np
from blackjack.players.bots.strategist_abc import Strategist

class StrategyDbGetters(object):
    """
    This class is responsible for all getter methods for strategy databases.
    """
    
    @classmethod
    def get_hard_total_matrix(cls, db_path) -> np.ndarray:
        """
        Returns values from the HardTotals table as a strategy matrix that conforms
        to the HardTotalStrategy matrix
        """
        connection = sqlite3.Connection(db_path)
        sql_statement = '''SELECT * FROM HardTotals ORDER BY PlayerScore DESC'''
        table_values = connection.execute(sql_statement).fetchall()
        connection.close()
        hard_total_matrix = np.zeros(shape=(18, 10), dtype=int)
        for row_number in range(18):
            for column_number in range(10):
                hard_total_matrix[row_number][column_number] = table_values[row_number][column_number + 1]
        return hard_total_matrix
    
    @classmethod
    def get_soft_total_matrix(cls, db_path) -> np.ndarray:
        """
        Returns values from the SoftTotals table as a strategy matrix that conforms
        to the SoftTotalStrategy matrix
        """
        connection = sqlite3.Connection(db_path)
        sql_statement = '''SELECT * FROM SoftTotals ORDER BY PlayerScore DESC'''
        table_values = connection.execute(sql_statement).fetchall()
        connection.close()
        soft_total_matrix = np.zeros(shape=(20, 10), dtype=int)
        for row_number in range(20):
            for column_number in range(10):
                soft_total_matrix[row_number][column_number] = table_values[row_number][column_number + 1]
        return soft_total_matrix
    
    @classmethod
    def get_split_pair_matrix(cls, db_path) -> np.ndarray:
        """
        Returns values from the SplitPairs table as a strategy matrix that conforms
        to the SoftTotalStrategy matrix
        """
        connection = sqlite3.Connection(db_path)
        sql_statement = '''SELECT * FROM SplitPairs ORDER BY PlayerScore DESC'''
        table_values = connection.execute(sql_statement).fetchall()
        connection.close()
        split_pair_matrix = np.zeros(shape=(10, 10), dtype=int)
        for row_number in range(10):
            for column_number in range(10):
                split_pair_matrix[row_number][column_number] = table_values[row_number][column_number + 1]
        return split_pair_matrix
    
    @classmethod
    def get_player_from_database(cls, db_path: str) -> Strategist:
        """
        Returns a bot with strategy matrixes that are fetched from strategy database tables.
        """
        player = Strategist("Retrieved Player")
        player.hard_total_strategy.set_strategy_matrix(StrategyDbGetters.get_hard_total_matrix(db_path))
        player.soft_total_strategy.set_strategy_matrix(StrategyDbGetters.get_soft_total_matrix(db_path))
        player.split_pair_strategy.set_strategy_matrix(StrategyDbGetters.get_split_pair_matrix(db_path))
        return player