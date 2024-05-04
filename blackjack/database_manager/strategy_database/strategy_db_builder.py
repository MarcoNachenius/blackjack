import sqlite3

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