import sqlite3
from blackjack.database_manager.strategy_database.strategy_db_builder import StrategyDbBuilder
from blackjack.database_manager.strategy_database.strategy_db_setters import StrategyDbSetters

class LearningBotDbBuilder(StrategyDbBuilder):
    
    @classmethod
    def create_learner_bot_database(cls, db_path: str):
        '''
        ## Database tables
        The learning bot database has the following tables:
        - IdealHardTotalsStrategy
        - IdealSoftTotalsStrategy
        - IdealSplitPairsStrategy
        - HardTotalsMemory
        - SoftTotalsMemory
        - SplitPairsMemory
        
        The learning bot database is an extended version of the strategy_database builder. 
        It creates the same three strategy tables that Strategist bots use, but includes another
        3 databases that track the use of every action number and the outcome of its use.
        
        
        ### IdealHardTotalsStrategy, IdealSoftTotalsStrategy and IdealSplitPairsStrategy tables
        #### Description
        These three tables are representations of ideal strategy matrixes. When the database is created
        for the first time, all of the action numbers in these tables will be 0.
        Action numbers of these matrixes are those which have had the highest amount
        of success. See strategy documentation of StrategyDbBuilder for more information about the dimensions, keys and values of these tables.
        
        #### Table values 
        - PlayerScore : INTEGER(PK-AI)
        - Ace :  INTEGER
        - Two :  INTEGER
        - Three :  INTEGER
        - Four :  INTEGER
        - Five :  INTEGER
        - Six :  INTEGER
        - Seven :  INTEGER
        - Eight :  INTEGER
        - Nine :  INTEGER
        - TenPointCard :  INTEGER
        #### Column values that remain constant once created
        - PlayerScore
        
        
        ### HardTotalsMemory, SoftTotalsMemory and SplitPairsMemory tables
        #### Description
        The primary purpose for these tables are to track the use and outcome of a action number when it is used.
        These three tables always have a fixed number of rows, although the amount of rows differ for every table. 
        
        #### Table values
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        
        #### Column values that remain constant once created
        - PlayerScore
        - DealerUpcardPoints
        - ActionNumber
        '''
        # Create populated HardTotals, SoftTotals and SplitPairs tables
        cls.create_zeroes_database(db_path)
        # Rename HardTotals, SoftTotals and SplitPairs tables
        connection = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        # Rename HardTotals to IdealHardTotalsStrategy
        cursor.execute('''ALTER TABLE HardTotals RENAME TO IdealHardTotalsStrategy''')
        connection.commit()
        # Rename SoftTotals to IdealSoftTotalsStrategy
        cursor.execute('''ALTER TABLE SoftTotals RENAME TO IdealSoftTotalsStrategy''')
        connection.commit()
        # Rename SplitPairs to IdealSplitPairsStrategy
        cursor.execute('''ALTER TABLE SplitPairs RENAME TO IdealSplitPairsStrategy''')
        connection.commit()
        
        # Create and populate HardTotalsMemory table
        cls.create_empty_hard_totals_memory_table(db_path)
        cls.populate_empty_hard_totals_memory_table(db_path)
        
        # Create and populate HardTotalsMemory table
        cls.create_empty_soft_totals_memory_table(db_path)
        cls.populate_empty_soft_totals_memory_table(db_path)
        
        # Create and populate HardTotalsMemory table
        cls.create_empty_split_pairs_memory_table(db_path)
        cls.populate_empty_split_pairs_memory_table(db_path)
    
    @classmethod
    def create_empty_hard_totals_memory_table(cls, db_path: str):
        """
        #### What it does
        Creates a table named HardTotalsMemory without any rows.
        
        #### Table keys
        HardTotalsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        # Build SQL command that creates HardTotalsMemory table
        create_hard_totals_sql = '''CREATE TABLE IF NOT EXISTS HardTotalsMemory (
                            LogID INTEGER PRIMARY KEY,
                            PlayerScore INTEGER,
                            DealerUpcardPoints INTEGER,
                            ActionNumber INTEGER,
                            Trials INTEGER,
                            OutcomeScore INTEGER
                            )'''
        # Execute SQL command
        cursor.execute(create_hard_totals_sql)
        cursor.connection.commit()
        # Close connection to database
        connection.close()
    
    @classmethod
    def create_empty_soft_totals_memory_table(cls, db_path: str):
        """
        #### What it does
        Creates a table named SoftTotalsMemory without any rows.
        
        #### Table keys
        SoftTotalsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        # Build SQL command that creates SoftTotalsMemory table
        create_soft_totals_sql = '''CREATE TABLE IF NOT EXISTS SoftTotalsMemory (
                            LogID INTEGER PRIMARY KEY,
                            PlayerScore INTEGER,
                            DealerUpcardPoints INTEGER,
                            ActionNumber INTEGER,
                            Trials INTEGER,
                            OutcomeScore INTEGER
                            )'''
        # Execute SQL command
        cursor.execute(create_soft_totals_sql)
        cursor.connection.commit()
        # Close connection to database
        connection.close()
    
    @classmethod
    def create_empty_split_pairs_memory_table(cls, db_path: str):
        """
        #### What it does
        Creates a table named SplitPairsMemory without any rows.
        
        #### Table keys
        SplitPairsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        # Build SQL command that creates SplitPairsMemory table
        create_split_pairs_sql = '''CREATE TABLE IF NOT EXISTS SplitPairsMemory (
                            LogID INTEGER PRIMARY KEY,
                            PlayerScore INTEGER,
                            DealerUpcardPoints INTEGER,
                            ActionNumber INTEGER,
                            Trials INTEGER,
                            OutcomeScore INTEGER
                            )'''
        # Execute SQL command
        cursor.execute(create_split_pairs_sql)
        cursor.connection.commit()
        # Close connection to database
        connection.close()
    
    @classmethod
    def populate_empty_hard_totals_memory_table(cls, db_path: str):
        """
        #### What it does
        Populates empty HardTotalsMemory table where all Trials and OutcomeScore values are set to 0.
        
        #### Column values that remain constant once created
        - PlayerScore
        - DealerUpcardPoints
        - ActionNumber
        
        #### Table keys
        HardTotalsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        player_score_index_number_to_score = StrategyDbSetters.HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE
        # Set iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(18))
        z_coordinate_index_range = list(range(8))
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Build SQL command that creates HardTotalsMemory table
                    insert_into_hard_totals_memory_sql = '''INSERT INTO HardTotalsMemory(PlayerScore, DealerUpcardPoints, ActionNumber, Trials, OutcomeScore) VALUES(?,?,?,?,?)'''
                    # Execute SQL command
                    player_score = player_score_index_number_to_score[y_coordinate]
                    dealer_upcard_score = x_coordinate + 1
                    action_number = z_coordinate
                    cursor.execute(insert_into_hard_totals_memory_sql, (player_score, dealer_upcard_score, action_number, 0, 0))
        cursor.connection.commit()
        
        # Close connection to database
        connection.close()
    
    @classmethod
    def populate_empty_soft_totals_memory_table(cls, db_path: str):
        """
        #### What it does
        Populates empty SoftTotalsMemory table where all Trials and OutcomeScore values are set to 0.
        
        #### Column values that remain constant once created
        - PlayerScore
        - DealerUpcardPoints
        - ActionNumber
        
        #### Table keys
        SoftTotalsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        player_score_index_number_to_score = StrategyDbSetters.SOFT_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE
        # Set iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(20))
        z_coordinate_index_range = list(range(8))
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Build SQL command that creates SoftTotalsMemory table
                    insert_into_soft_totals_memory_sql = '''INSERT INTO SoftTotalsMemory(PlayerScore, DealerUpcardPoints, ActionNumber, Trials, OutcomeScore) VALUES(?,?,?,?,?)'''
                    # Execute SQL command
                    player_score = player_score_index_number_to_score[y_coordinate]
                    dealer_upcard_score = x_coordinate + 1
                    action_number = z_coordinate
                    cursor.execute(insert_into_soft_totals_memory_sql, (player_score, dealer_upcard_score, action_number, 0, 0))
        cursor.connection.commit()
        
        # Close connection to database
        connection.close()
    
    @classmethod
    def populate_empty_split_pairs_memory_table(cls, db_path: str):
        """
        #### What it does
        Populates empty SplitPairsMemory table where all Trials and OutcomeScore values are set to 0.
        
        #### Column values that remain constant once created
        - PlayerScore
        - DealerUpcardPoints
        - ActionNumber
        
        #### Table keys
        SplitPairsMemory table has the following columns:
        - LogID : INTEGER(PK-AI)
        - PlayerScore : INTEGER
        - DealerUpcardPoints : INTEGER
        - ActionNumber : INTEGER
        - Trials : INTEGER
        - OutcomeScore : INTEGER
        """
        player_score_index_number_to_score = StrategyDbSetters.SPLIT_PAIR_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE
        # Set iteration ranges
        x_coordinate_index_range = list(range(10))
        y_coordinate_index_range = list(range(10))
        z_coordinate_index_range = list(range(2))
        # Establish connection to database
        connection  = sqlite3.Connection(db_path)
        # Initialize cursor
        cursor = connection.cursor()
        for x_coordinate in x_coordinate_index_range:
            for y_coordinate in y_coordinate_index_range:
                for z_coordinate in z_coordinate_index_range:
                    # Build SQL command that creates SplitPairsMemory table
                    insert_into_split_pairs_memory_sql = '''INSERT INTO SplitPairsMemory(PlayerScore, DealerUpcardPoints, ActionNumber, Trials, OutcomeScore) VALUES(?,?,?,?,?)'''
                    # Execute SQL command
                    player_score = player_score_index_number_to_score[y_coordinate]
                    dealer_upcard_score = x_coordinate + 1
                    action_number = z_coordinate
                    cursor.execute(insert_into_split_pairs_memory_sql, (player_score, dealer_upcard_score, action_number, 0, 0))
        cursor.connection.commit()
        
        # Close connection to database
        connection.close()