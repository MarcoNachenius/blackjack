import unittest
from blackjack.database_manager.db_builder import DatabaseBuilder
from blackjack.database_manager.db_setters import DatabaseSetters

class test_database_updates(unittest.TestCase):
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