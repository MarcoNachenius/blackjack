import sqlite3
# Bots
from blackjack.players.bots.strategist_abc import Strategist
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
# Db objects
from blackjack.database_manager.strategy_database.strategy_db_setters import StrategyDbSetters

class StrategyDbBuilder(object):
    
    """
    This class is responsible for creating all databases and tables that act as a method of record keeping for strategy matrixes
    during the execution of simulations
    """
    
    
    @classmethod
    def create_empty_database(cls, db_path: str):
        """
        Creates an empty database with HardTotals, SoftTotals and SplitPairs tables based on the provided path to the db.
        """
        cls.crete_empty_hard_totals_table(db_path)
        cls.crete_empty_soft_totals_table(db_path)
        cls.crete_empty_split_pairs_table(db_path)
        
    @classmethod
    def crete_empty_hard_totals_table(cls, db_path: str):
        """
        Creates HardTotals table within a given database. If the provided database already contains
        a HardTotals table, the creation of the HardTotal table will be terminal.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        create_hard_totals_sql = '''CREATE TABLE IF NOT EXISTS HardTotals (
                            PlayerScore INTEGER PRIMARY KEY,
                            Ace INTEGER,
                            Two INTEGER,
                            Three INTEGER,
                            Four INTEGER,
                            Five INTEGER,
                            Six INTEGER,
                            Seven INTEGER,
                            Eight INTEGER,
                            Nine INTEGER,
                            TenPointCard INTEGER
                            )'''
        cursor.execute(create_hard_totals_sql)
        cursor.connection.commit()
        connection.close()
    
    @classmethod
    def crete_empty_soft_totals_table(cls, db_path: str):
        """
        Creates HardTotals table within a given database. If the provided database already contains
        a HardTotals table, the creation of the HardTotal table will be terminal.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        create_hard_totals_sql = '''CREATE TABLE IF NOT EXISTS SoftTotals (
                            PlayerScore INTEGER PRIMARY KEY,
                            Ace INTEGER,
                            Two INTEGER,
                            Three INTEGER,
                            Four INTEGER,
                            Five INTEGER,
                            Six INTEGER,
                            Seven INTEGER,
                            Eight INTEGER,
                            Nine INTEGER,
                            TenPointCard INTEGER
                            )'''
        cursor.execute(create_hard_totals_sql)
        cursor.connection.commit()
        connection.close()
    
    @classmethod
    def crete_empty_split_pairs_table(cls, db_path: str):
        """
        Creates HardTotals table within a given database. If the provided database already contains
        a HardTotals table, the creation of the HardTotal table will be terminal.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        
        create_hard_totals_sql = '''CREATE TABLE IF NOT EXISTS SplitPairs (
                            PlayerScore INTEGER PRIMARY KEY,
                            Ace INTEGER,
                            Two INTEGER,
                            Three INTEGER,
                            Four INTEGER,
                            Five INTEGER,
                            Six INTEGER,
                            Seven INTEGER,
                            Eight INTEGER,
                            Nine INTEGER,
                            TenPointCard INTEGER
                            )'''
        cursor.execute(create_hard_totals_sql)
        cursor.connection.commit()
        connection.close()
        
    @classmethod
    def create_zeroes_database(cls, db_path: str):
        """
        Creates a database where the HardTotals, SoftTotals and SplitPairs tables are populated with zeroes. 
        """
        zeroes_bot = Strategist(player_name="Zeroes Strategist")
        cls.create_empty_database(db_path)
        cls.crete_empty_hard_totals_table(db_path)
        cls.crete_empty_soft_totals_table(db_path)
        cls.crete_empty_split_pairs_table(db_path)
        StrategyDbSetters.insert_matrix_into_empty_hard_totals_table(db_path=db_path, hard_total_matrix=zeroes_bot.hard_total_strategy.get_strategy_matrix())
        StrategyDbSetters.insert_matrix_into_empty_soft_totals_table(db_path=db_path, soft_total_matrix=zeroes_bot.soft_total_strategy.get_strategy_matrix())
        StrategyDbSetters.insert_matrix_into_empty_split_pairs_table(db_path=db_path, split_pair_matrix=zeroes_bot.split_pair_strategy.get_strategy_matrix())
    
    @classmethod
    def create_perfect_strategist_database(cls, db_path: str):
        """
        Creates a database where the HardTotals, SoftTotals and SplitPairs tables are populated with strategy matrixes of the PerfectStrategist bot. 
        """
        perfect_strategist = PerfectStrategist(player_name="Perfect Strategist")
        cls.create_empty_database(db_path)
        cls.crete_empty_hard_totals_table(db_path)
        cls.crete_empty_soft_totals_table(db_path)
        cls.crete_empty_split_pairs_table(db_path)
        StrategyDbSetters.insert_matrix_into_empty_hard_totals_table(db_path=db_path, hard_total_matrix=perfect_strategist.hard_total_strategy.get_strategy_matrix())
        StrategyDbSetters.insert_matrix_into_empty_soft_totals_table(db_path=db_path, soft_total_matrix=perfect_strategist.soft_total_strategy.get_strategy_matrix())
        StrategyDbSetters.insert_matrix_into_empty_split_pairs_table(db_path=db_path, split_pair_matrix=perfect_strategist.split_pair_strategy.get_strategy_matrix())