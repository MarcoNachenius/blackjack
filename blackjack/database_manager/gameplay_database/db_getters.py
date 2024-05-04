import sqlite3
from pathlib import Path

class DatabaseGetters(object):
    """
    This class contains all of the getters for table values.
    
    As a general rule, names follow the following convention:
        <table_name>_<db_operation_name>
    For example, the method that retrieves the balance of a player from the 'Players' table of
    the database has the following name:
        players_get_balance_by_player_id
    """

    def __init__(self, db_name = 'blackjack.db', base_dir = None) -> None:
        self.db_name = db_name
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.connection = sqlite3.Connection(self.base_dir / self.db_name)
        self.cursor = self.connection.cursor()
    
    def players_get_balance_by_player_id(self, player_id: int) -> int:
        sql_statement = '''SELECT Balance FROM Players WHERE PlayerID LIMIT 1 = ?'''
        return self.connection.execute(sql_statement, (player_id,)).fetchone()[0]