import unittest
import os

# BOTS
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
from blackjack.players.bots.strategist_abc import Strategist
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
    
    def test_replace_hard_totals_table_values(self):
        
        db_path = 'test.db'
        StrategyDbBuilder.create_zeroes_database(db_path)
        perfect_strategist = PerfectStrategist()
        zeroes_bot = Strategist("Zeroes")
        
        # Confirm initial state
        self.assertEqual(zeroes_bot.hard_total_strategy.get_strategy_matrix().all(), StrategyDbGetters.get_hard_total_matrix(db_path).all())
        # Perform table value replacement
        StrategyDbSetters.replace_hard_totals_table(db_path=db_path, hard_total_matrix=perfect_strategist.hard_total_strategy.get_strategy_matrix())
        # Test successful change of values
        self.assertEqual(StrategyDbGetters.get_hard_total_matrix(db_path).all(), perfect_strategist.hard_total_strategy.get_strategy_matrix().all())
        os.remove(db_path)
        
    def test_replace_soft_totals_table_values(self):
        
        db_path = 'test.db'
        StrategyDbBuilder.create_zeroes_database(db_path)
        perfect_strategist = PerfectStrategist()
        zeroes_bot = Strategist("Zeroes")
        
        # Confirm initial state
        self.assertEqual(zeroes_bot.soft_total_strategy.get_strategy_matrix().all(), StrategyDbGetters.get_soft_total_matrix(db_path).all())
        # Perform table value replacement
        StrategyDbSetters.replace_soft_totals_table(db_path=db_path, soft_total_matrix=perfect_strategist.soft_total_strategy.get_strategy_matrix())
        # Test successful change of values
        self.assertEqual(StrategyDbGetters.get_soft_total_matrix(db_path).all(), perfect_strategist.soft_total_strategy.get_strategy_matrix().all())
        os.remove(db_path)
        
    def test_replace_split_pairs_table_values(self):
        
        db_path = 'test.db'
        StrategyDbBuilder.create_zeroes_database(db_path)
        perfect_strategist = PerfectStrategist()
        zeroes_bot = Strategist("Zeroes")
        
        # Confirm initial state
        self.assertEqual(zeroes_bot.split_pair_strategy.get_strategy_matrix().all(), StrategyDbGetters.get_split_pair_matrix(db_path).all())
        # Perform table value replacement
        StrategyDbSetters.replace_split_pairs_table(db_path=db_path, split_pair_matrix=perfect_strategist.split_pair_strategy.get_strategy_matrix())
        # Test successful change of values
        self.assertEqual(StrategyDbGetters.get_split_pair_matrix(db_path).all(), perfect_strategist.split_pair_strategy.get_strategy_matrix().all())
        os.remove(db_path)
        
    
    def test_get_player_from_database(self):
        db_path = 'test.db'
        StrategyDbBuilder.create_perfect_strategist_database(db_path)
        perfect_strategist = PerfectStrategist()
        retrieved_player = StrategyDbGetters.get_player_from_database(db_path)
        self.assertEqual(perfect_strategist.hard_total_strategy.get_strategy_matrix().all(), retrieved_player.hard_total_strategy.get_strategy_matrix().all())
        self.assertEqual(perfect_strategist.soft_total_strategy.get_strategy_matrix().all(), retrieved_player.soft_total_strategy.get_strategy_matrix().all())
        self.assertEqual(perfect_strategist.split_pair_strategy.get_strategy_matrix().all(), retrieved_player.split_pair_strategy.get_strategy_matrix().all())
        os.remove(db_path)