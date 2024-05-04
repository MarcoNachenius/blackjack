import sqlite3
from pathlib import Path

class DatabaseSetters(object):
    """
    This class is responsible for changing values in the database once it has been created.
    
    As a general rule, names follow the following convention:
        <table_name>_<db_operation_name>
    For example, the method that changes the balance of a player in the 'Players' table of
    the database has the following name:
        players_set_balance_by_player_id
    """

    def __init__(self, db_name = 'blackjack.db', base_dir = None) -> None:
        self.db_name = db_name
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.connection = sqlite3.Connection(self.base_dir / self.db_name)
        self.cursor = self.connection.cursor()
    
    def players_set_balance_by_player_id(self, player_id: int, balance: int):
        """
        Changes 'Balance' value based on the provided player id.
        player_id must correspond with an existing 'PlayerID' in the 'Players' table.
        """
        sql_statement = '''UPDATE Players
                           SET Balance = ?
                           WHERE PlayerID = ?
                        '''
        self.cursor.execute(sql_statement, (balance, player_id))
        self.connection.commit()