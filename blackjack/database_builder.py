import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
conn = sqlite3.Connection(BASE_DIR / 'blackjack.db')
cur = conn.cursor()

def create_database():
    create_handcombos_table = '''CREATE TABLE handcombos (
                        HandComboID INT AUTO_INCREMENT,
                        IsDoubledDown VARCHAR(10),
                        Outcome VARCHAR(20),
                        PRIMARY KEY (HandComboID)
                        )'''
    cur.execute(create_handcombos_table)

    create_hands_table = '''CREATE TABLE hands (
                        HandID INT AUTO_INCREMENT,
                        Rank VARCHAR(45),
                        Suite VARCHAR(45),
                        Points INT, 
                        PRIMARY KEY (HandID)
                        )'''
    cur.execute(create_hands_table)

    create_players_table = '''CREATE TABLE players (
                        PlayerID VARCHAR(100) PRIMARY KEY,
                        Balance INT
                        )'''
    cur.execute(create_players_table)

    create_round_players_table = '''CREATE TABLE roundplayers (
                        ParticipatingPlayersID INT AUTO_INCREMENT,
                        PlayerID INT,
                        HandComboID INT,
                        InitialBetAmount INT,
                        TotalWinnings INT,
                        PRIMARY KEY (ParticipatingPlayersID)
                        )'''
    cur.execute(create_round_players_table)

    create_rounds_table = '''CREATE TABLE rounds (
                        RoundID INT AUTO_INCREMENT,
                        GameID INT,
                        ParticipatingPlayersID INT,
                        DealerHandID INT,
                        PRIMARY KEY (RoundID)
                        )'''
    cur.execute(create_rounds_table)

insert_command = '''INSERT INTO all_values (
                row_number,
                prime_row,
                prime_retrograde,
                prime_inversion,
                prime_retrograde_inversion,
                prime_row_intervals,
                prime_retrograde_intervals,
                prime_inversion_intervals,
                prime_retrograde_inversion_intervals,
                combinatorial_hexachords,
                combinatorial_tetrachords,
                combinatorial_trichords
                )
                VALUES (
                ?, --row_number,
                ?, --prime_row,
                ?, --prime_retrograde,
                ?, --prime_inversion,
                ?, --prime_retrograde_inversion,
                ?, --prime_row_intervals,
                ?, --prime_retrograde_intervals,
                ?, --prime_inversion_intervals,
                ?, --prime_retrograde_inversion_intervals,
                ?, --combinatorial_hexachords,
                ?, --combinatorial_tetrachords,
                ?  --combinatorial_trichords
                )''' 

create_database()