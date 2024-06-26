import unittest
from blackjack.database_manager.gameplay_database.db_builder import DatabaseBuilder
from blackjack.database_manager.strategy_database.strategy_db_builder import StrategyDbBuilder
import os

class TestGameplayDbCreation(unittest.TestCase):
    
    def test_gameplay_database_creation(self):
        database = DatabaseBuilder(db_name='test_database.db')
        database.create_database()
        amount_of_rows = 5
        for i in range(amount_of_rows):
            database.insert_into_games()
            database.insert_into_rounds(game_id=500, dealer_hand_id=50)
            database.insert_into_players()
            database.insert_into_player_history(player_id=100, round_id=50)
            database.insert_into_hand_history(hand_combo_id=10)
            database.insert_into_card_history(hand_id=50)

        self.assertEqual(database.get_last_id_games(), amount_of_rows)
        self.assertEqual(database.get_last_id_rounds(), amount_of_rows)
        self.assertEqual(database.get_last_id_players(), amount_of_rows)
        self.assertEqual(database.get_last_hand_combo(), amount_of_rows)
        self.assertEqual(database.get_last_hand_id(), amount_of_rows)
        self.assertEqual(database.get_last_card_id(), amount_of_rows)

        database.connection.close()
        database.delete_database()


class TestSimulationDbCreation(unittest.TestCase):
    
    def test_strategy_database_creation(self):
        StrategyDbBuilder.create_empty_database('test_database.db')
        self.assertTrue(os.path.isfile('test_database.db'))
        os.remove('test_database.db')
    
    