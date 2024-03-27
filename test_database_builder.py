import unittest
from blackjack.database_builder import DatabaseBuilder
import os

class test_database_creation(unittest.TestCase):
    
    def test_database_creation(self):
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
        os.remove("./test_database.db")
    
    #def test_update_statements(self):
    #    database = DatabaseBuilder(db_name='test_database.db')
    #    database.create_database()
    #    
    #    # 
    #    database.insert_into_games()
    #    database.insert_into_rounds(50)
    #    database.insert_into_players()
    #    database.insert_into_player_history(player_id=100, round_id=50)
    #    database.insert_into_hand_history(hand_combo_id=10)
    #    database.insert_into_card_history(hand_id=50)