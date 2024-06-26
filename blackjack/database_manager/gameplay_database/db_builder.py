import sqlite3
from pathlib import Path
import os

class DatabaseBuilder(object):
    
    """
    This class is responsible for the creation of the database, tables, and table entries.
    """

    def __init__(self, db_name = 'blackjack.db', base_dir = None) -> None:
        self.db_name = db_name
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.connection = sqlite3.Connection(self.base_dir / self.db_name)
        self.cursor = self.connection.cursor()
    
    
    def create_database(self):
        """
        Creates database and all tables.
        """
        # GAMES TABLE
        create_games_table = '''CREATE TABLE Games (
                            GameID INTEGER PRIMARY KEY,
                            InProgress VARCHAR(10)
                            )'''
        self.cursor.execute(create_games_table)
        self.cursor.connection.commit()
        
        # ROUNDS TABLE
        create_rounds_table = '''CREATE TABLE Rounds (
                            RoundID INTEGER PRIMARY KEY,
                            GameID INTEGER,
                            DealerHandID INTEGER,
                            InProgress VARCHAR(10)
                            )'''
        self.cursor.execute(create_rounds_table)
        self.cursor.connection.commit()
        
        # PLAYERS TABLE
        create_players_table = '''CREATE TABLE Players (
                            PlayerID INTEGER PRIMARY KEY,
                            PlayerName VARCHAR(100),
                            Balance INTEGER
                            )'''
        self.cursor.execute(create_players_table)
        self.cursor.connection.commit()
        
        # PLAYERHISTORY TABLE
        create_player_history_table = '''CREATE TABLE PlayerHistory (
                            HandComboID INTEGER PRIMARY KEY,
                            PlayerID INTEGER,
                            RoundID INTEGER,
                            IsInsured VARCHAR(10),
                            InitialBet INTEGER
                            )'''
        self.cursor.execute(create_player_history_table)
        self.cursor.connection.commit()
        
        # HANDHISTORY TABLE
        create_hand_history_table = '''CREATE TABLE HandHistory (
                            HandID INTEGER PRIMARY KEY,
                            HandComboID INTEGER,
                            IsDoubledDown VARCHAR(10),
                            Outcome VARCHAR(100)
                            )'''
        self.cursor.execute(create_hand_history_table)
        self.cursor.connection.commit()
        
        # CARDHISTORY TABLE
        create_card_history_table = '''CREATE TABLE CardHistory (
                            CardID INTEGER PRIMARY KEY,
                            HandID INTEGER,
                            CardName VARCHAR(100)
                            )'''
        self.cursor.execute(create_card_history_table)
        self.cursor.connection.commit()

    # GAMES
    def insert_into_games(self, in_progress = "True"):
        """
        Adds row to Games table. 
        GameID will be added as AI-PK.
        """
        sql_command ='''INSERT INTO Games(InProgress)
                        VALUES(?)'''
        self.connection.execute(sql_command, (in_progress,))
        self.connection.commit() 
    def get_last_id_games(self) -> int:
       last_game_id = self.connection.execute("SELECT * FROM Games ORDER BY GameID DESC LIMIT 1;").fetchone()
       self.connection.commit()
       return last_game_id[0]
    
    # ROUNDS
    def insert_into_rounds(self, game_id: int, dealer_hand_id: int, in_progress = "True"):
        """
        Adds row to Rounds table. 
        RoundID will be added as AI-PK.
        """
        sql_command ='''INSERT INTO Rounds(GameID, DealerHandID, InProgress)
                        VALUES(?,?,?)'''
        self.connection.execute(sql_command, (game_id, dealer_hand_id, in_progress))
        self.connection.commit() 
    def get_last_id_rounds(self) -> int:
       last_game_id = self.connection.execute("SELECT * FROM Rounds ORDER BY RoundID DESC LIMIT 1;").fetchone()
       self.connection.commit()
       return last_game_id[0]

    # PLAYERS
    def insert_into_players(self, player_name = "TEST PLAYER", balance = 1000):
        """
        Adds row to Players table. 
        PlayerID will be added as AI-PK.
        """
        sql_command ='''INSERT INTO Players(PlayerName, Balance)
                        VALUES(?,?)'''
        self.connection.execute(sql_command, (player_name, balance))
        self.connection.commit() 
    def get_last_id_players(self) -> int:
       last_game_id = self.connection.execute("SELECT * FROM Players ORDER BY PlayerID DESC LIMIT 1;").fetchone()
       self.connection.commit()
       return last_game_id[0]
   
    # PLAYER_HISTORY
    def insert_into_player_history(self, player_id: int, round_id: int, is_insured: str = "False", initial_bet: int = 0):
        """
        Adds row to PlayerHistory table. 
        HandComboID will be added as AI-PK.
        """
        sql_command ='''INSERT INTO PlayerHistory(PlayerID, RoundID, IsInsured, InitialBet)
                        VALUES(?,?,?,?)'''
        self.connection.execute(sql_command, (player_id, round_id, is_insured, initial_bet))
        self.connection.commit() 
    def get_last_hand_combo(self) -> int:
        """
        Returns last value of HandComboID in PlayerHistory table
        """
        last_hand_combo_id = self.connection.execute("SELECT * FROM PlayerHistory ORDER BY HandComboID DESC LIMIT 1;").fetchone()
        self.connection.commit()
        return last_hand_combo_id[0]
    
    # HAND_HISTORY
    def insert_into_hand_history(self, hand_combo_id: int, is_doubled_down: str = "False", outcome: str = ""):
        """
        Adds row to HandHistory table. 
        HandID will be added as AI-PK.
        HandComID == 0 means that it is a dealer hand.
        """
        sql_command ='''INSERT INTO HandHistory(HandComboID, IsDoubledDown, Outcome)
                        VALUES(?,?,?)'''
        self.connection.execute(sql_command, (hand_combo_id, is_doubled_down, outcome))
        self.connection.commit() 
    def get_last_hand_id(self) -> int:
        """
        Returns last value of HandID in HandHistory table
        """
        last_hand_id = self.connection.execute("SELECT * FROM HandHistory ORDER BY HandID DESC LIMIT 1;").fetchone()
        self.connection.commit()
        return last_hand_id[0]
    
    # CARD_HISTORY
    def insert_into_card_history(self, hand_id: int, card_name: str = ""):
        """
        Adds row to CardHistory table. 
        CardID will be added as AI-PK.
        """
        sql_command ='''INSERT INTO CardHistory(HandID, CardName)
                        VALUES(?,?)'''
        self.connection.execute(sql_command, (hand_id, card_name))
        self.connection.commit() 
    def get_last_card_id(self) -> int:
        """
        Returns last value of CardID in CardHistory table
        """
        last_card_id = self.connection.execute("SELECT * FROM CardHistory ORDER BY CardID DESC LIMIT 1;").fetchone()
        self.connection.commit()
        return last_card_id[0]

    def delete_database(self):
        """
        Deletes database from pre-defined dir and db name
        """
        os.remove(self.base_dir / self.db_name)
