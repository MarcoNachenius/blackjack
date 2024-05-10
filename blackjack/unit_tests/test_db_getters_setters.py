import unittest
import os

# PS MATRIXES
import players.bots.perfect_strategist.strategy_matrixes as ps_strategy_matrixes
# GAMEPLAY DATABASE
from database_manager.gameplay_database.db_builder import DatabaseBuilder
from database_manager.gameplay_database.db_setters import DatabaseSetters
# STRATEGY DATABASE
from database_manager.strategy_database.strategy_db_getters import StrategyDbGetters
from database_manager.strategy_database.strategy_db_setters import StrategyDbSetters
from database_manager.strategy_database.strategy_db_builder import StrategyDbBuilder

class TestGameplayDatabaseUpdates(unittest.TestCase):
    """
    Tests all setters for existing database entries
    """
    def test_players_set_balance_by_player_id(self):
        # Create test objects
        test_database = DatabaseBuilder(db_name="test_db_updater.db")
        test_database.create_database()
        db_setters = DatabaseSetters(db_name=test_database.db_name)
        
        # Insert two players into Players table
        test_database.insert_into_players(balance=100)
        test_database.insert_into_players(balance=100)
        # Change balance of second player
        db_setters.players_set_balance_by_player_id(player_id=2, balance=50)
        # Close connections and delete database
        test_database.connection.close()
        db_setters.connection.close()
        test_database.delete_database()
        
class TestStrategyDatabase(unittest.TestCase):
    
    def test_get_and_set_strategy_database(self):
        
        db_path = 'test.db'
        StrategyDbBuilder.create_empty_database(db_path)
        # Insert values into tables
        StrategyDbSetters.insert_matrix_into_empty_hard_totals_table(db_path=db_path, hard_total_matrix=ps_strategy_matrixes.hard_totals)
        StrategyDbSetters.insert_matrix_into_empty_soft_totals_table(db_path=db_path, soft_total_matrix=ps_strategy_matrixes.soft_totals)
        StrategyDbSetters.insert_matrix_into_empty_split_pairs_table(db_path=db_path, split_pair_matrix=ps_strategy_matrixes.split_pairs)
        # Test getters
        self.assertEqual(StrategyDbGetters.get_hard_total_matrix(db_path=db_path).all(), ps_strategy_matrixes.hard_totals.all())
        self.assertEqual(StrategyDbGetters.get_soft_total_matrix(db_path=db_path).all(), ps_strategy_matrixes.soft_totals.all())
        self.assertEqual(StrategyDbGetters.get_split_pair_matrix(db_path=db_path).all(), ps_strategy_matrixes.split_pairs.all())
        os.remove(db_path)
        