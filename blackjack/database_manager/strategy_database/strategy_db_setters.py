import sqlite3
import numpy as np


class StrategyDbSetters(object):
    
    HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE ={
        0 : 21,
        1 : 20,
        2 : 19,
        3 : 18,
        4 : 17,
        5 : 16,
        6 : 15,
        7 : 14,
        8 : 13,
        9 : 12,
        10 : 11,
        11 : 10,
        12 : 9,
        13 : 8,
        14 : 7,
        15 : 6,
        16 : 5,
        17 : 4
    }
    @classmethod
    def insert_matrix_into_empty_hard_totals_table(cls, db_path, hard_total_matrix: np.ndarray):
        """
        Adds rows to empty HardTable table based on provided hard total strategy matrix and path to the db.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        for i in range(18):
            sql_command ='''INSERT INTO HardTotals(PlayerScore, Ace, Two, Three, Four, Five, Six, Seven, Eight, Nine, TenPointCard)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
            row_values = hard_total_matrix[i]
            cursor.execute(sql_command, (cls.HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[i], int(row_values[0]), int(row_values[1]), int(row_values[2]), int(row_values[3]), int(row_values[4]), int(row_values[5]), int(row_values[6]), int(row_values[7]), int(row_values[8]), int(row_values[9])))
            cursor.connection.commit()
        connection.close()
    
    
    SOFT_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE = {
        0 : 21,
        1 : 20,
        2 : 19,
        3 : 18,
        4 : 17,
        5 : 16,
        6 : 15,
        7 : 14,
        8 : 13,
        9 : 12,
        10 : 11,
        11 : 10,
        12 : 9,
        13 : 8,
        14 : 7,
        15 : 6,
        16 : 5,
        17 : 4,
        18 : 3,
        19 : 2
    }
    @classmethod
    def insert_matrix_into_empty_soft_totals_table(cls, db_path, soft_total_matrix: np.ndarray):
        """
        Adds rows to empty HardTable table based on provided hard total strategy matrix and path to the db.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        for i in range(20):
            sql_command ='''INSERT INTO SoftTotals(PlayerScore, Ace, Two, Three, Four, Five, Six, Seven, Eight, Nine, TenPointCard)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
            row_values = soft_total_matrix[i]
            cursor.execute(sql_command, (cls.SOFT_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[i], int(row_values[0]), int(row_values[1]), int(row_values[2]), int(row_values[3]), int(row_values[4]), int(row_values[5]), int(row_values[6]), int(row_values[7]), int(row_values[8]), int(row_values[9])))
            cursor.connection.commit()
        connection.close()


    SPLIT_PAIR_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE = {
        0 : 2,
        1 : 20,
        2 : 18,
        3 : 16,
        4 : 14,
        5 : 12,
        6 : 10,
        7 : 8,
        8 : 6,
        9 : 4
    }
    @classmethod
    def insert_matrix_into_empty_split_pairs_table(cls, db_path, split_pair_matrix: np.ndarray):
        """
        Adds rows to empty HardTable table based on provided hard total strategy matrix and path to the db.
        """
        connection  = sqlite3.Connection(db_path)
        cursor = connection.cursor()
        for i in range(10):
            sql_command ='''INSERT INTO SoftTotals(PlayerScore, Ace, Two, Three, Four, Five, Six, Seven, Eight, Nine, TenPointCard)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
            row_values = split_pair_matrix[i]
            cursor.execute(sql_command, (cls.SPLIT_PAIR_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE[i], int(row_values[0]), int(row_values[1]), int(row_values[2]), int(row_values[3]), int(row_values[4]), int(row_values[5]), int(row_values[6]), int(row_values[7]), int(row_values[8]), int(row_values[9])))
            cursor.connection.commit()
        connection.close()