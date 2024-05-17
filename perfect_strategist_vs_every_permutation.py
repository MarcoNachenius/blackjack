import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
from blackjack.players.bots.bot_builder import BotBuilder
from blackjack.players.bots.strategist_abc import Strategist
from blackjack.database_manager.strategy_database.strategy_db_builder import StrategyDbBuilder
from blackjack.database_manager.strategy_database.strategy_db_getters import StrategyDbGetters
from blackjack.database_manager.strategy_database.strategy_db_setters import StrategyDbSetters

def start_simulations():
    '''
    ## Description
    This method tests every possible permutation of the hard total, soft total and split pair
    matrixes as a collective unit, starting with all-zeroes values. Once a group of matrixes has been tested,
    every matrix will be moved up a step to the next permutation.
    
    Iterating through every possible permutation of theses strategy matrixes is a highly time-consuming task.
    It would be unrealistic and unreliable to expect that this function could test all permutations in a
    single run, as there are 7^(20*18)*(2^10) unique permutations. In order to avoid running tests from scratch 
    again every time this method is called, it will create a series of small databases as a mechanism to keep 
    track of which permutations have already been tested and document noteworthy results.
    
    ## Database creation
    ### Permutation memory
    Description:
    Stores the last permutation of the strategy matrix that has been tested. Whenever the method is stopped and
    started again, the permutations will be retrieved from this database and the method will continue testing 
    permutations from the values stored in the database.
    Path:\n
    /shared_files/databases/progress_storage/ps_vs_every_permutation.db
    
    

    ## Rules
    - Every player has the same number of chips at the start of every game
    - The first player to win a 7 games is the winner
    - A game is won when one of the players goes broke, or when one of the players has the most chips within a maximum number of rounds.
    - If a game end in a draw where both players have the same amount of remaining chips, a win will be awarded to the competing player.
    '''
    db_path = "./shared_files/databases/progress_storage/ps_vs_every_permutation.db"
    # Create database if it does not exist
    if not os.path.isfile(db_path):
        StrategyDbBuilder.create_zeroes_database(db_path)
    
    # Create bot with initial strategy values from database
    permutation_bot = StrategyDbGetters.get_player_from_database(db_path)
    
    # PRINT VALUES
    refresh_rate = 1# Game results are printed after specified amount of simulations
    database_update_rate = 100 
    # GAME VALUES
    best_out_of = 7 
    max_number_of_rounds = 200
    rounds_played = 0
    winner = None
    # SIMULATION RESULTS
    total_rounds = 0
    total_games = 0
    total_simulations = 0
    
    players_that_beat_perfect_strategist = 0
    worthy_competitors = 0
    # PRINT VALUES
    last_ht_matrix = None
    last_st_matrix = None
    last_sp_matrix = None
    
    while True:
        games_won_by_perfect_strategist = 0
        games_won_by_next_permutation_bot = 0
        total_simulations += 1
        
        while games_won_by_perfect_strategist < best_out_of and  games_won_by_next_permutation_bot < best_out_of:
            # Create game and player objects
            next_permutation_bot = BotBuilder.return_next_permutation_player(permutation_bot)
            permutation_bot = next_permutation_bot
            perfect_strategist = PerfectStrategist()
            
            # These matrixes are only used for print statements
            last_ht_matrix = next_permutation_bot.hard_total_strategy.get_strategy_matrix()
            last_st_matrix = next_permutation_bot.soft_total_strategy.get_strategy_matrix()
            last_sp_matrix = next_permutation_bot.split_pair_strategy.get_strategy_matrix()
            
            # Initiate new game object
            game = Game([next_permutation_bot, perfect_strategist])
            # Increase total number of games
            total_games += 1
            # If game ends before max number of rounds, a winner will be placed here
            premature_game_winner = None 
            
            while rounds_played != max_number_of_rounds:
                
                game.start_new_round()
                # Increase round counts
                rounds_played += 1
                total_rounds += 1
                # Check for winner
                if len(game.current_round.get_participating_players()) == 1:
                    premature_game_winner = game.current_round.get_participating_players()[0]
                    if premature_game_winner.get_player_name() == "Perfect Strategist":
                        games_won_by_perfect_strategist += 1
                    else:
                        games_won_by_next_permutation_bot += 1
                    break
                # Check for max round limit
                if rounds_played < max_number_of_rounds:
                    game.current_round.clear_round_values(dealer=game.get_dealer())
            
            # Check for winner when max round amount is reached
            if len(game.current_round.get_participating_players()) == 2:
                if perfect_strategist.get_chips() > next_permutation_bot.get_chips():
                    games_won_by_perfect_strategist += 1
                else:
                    games_won_by_next_permutation_bot += 1
                
            rounds_played = 0
        
        if total_simulations == 1 or total_simulations % database_update_rate == 0:
            StrategyDbSetters.replace_all_tables_with_bot_matrixes(db_path=db_path, bot=next_permutation_bot)
        
        # Print results every 5 times
        if total_simulations == 1 or total_simulations % refresh_rate == 0:
            os.system('clear')
            print("*********************************************************************")
            print("         PERFECT STRATEGIST VS EVERY POSSIBLE STRATEGY")
            print("*********************************************************************\n")
            print(f'RESULTS FOR SIMULATION {total_simulations}')
            print("=====================================================================")
            print("Player scores:")
            print(f'    Perfect Strategist: {games_won_by_perfect_strategist}')
            print(f'    Random Strategist: {games_won_by_next_permutation_bot}\n')
            print(f'  SOFT TOTAL MATRIX       HARD TOTAL MATRIX       SPLIT PAIR MATRIX')
            for i in range(len(last_st_matrix)):
                if i < 10:
                    print(f'{last_st_matrix[i]}   {last_ht_matrix[i]}   {last_sp_matrix[i]}')
                    continue
                if i < 18:
                    print(f'{last_st_matrix[i]}   {last_ht_matrix[i]}')
                    continue
                print(f'{last_st_matrix[i]}')
            print("=====================================================================\n")
            print("PROGRESS REPORT")
            print("=====================================================================")
            print(f'Total rounds: {total_rounds}')
            print(f'Total games: {total_games}')
            print(f'Total simulations: {total_simulations}')
            print(f'Superior strategists found: {players_that_beat_perfect_strategist}')
            print(f'Worthy competitors found: {worthy_competitors}')
            print("=====================================================================")
            
        
        
        # Add results to matrixes_that_beat_the_goat.txt if player beats perfect strategist
        if games_won_by_next_permutation_bot > games_won_by_perfect_strategist:
            players_that_beat_perfect_strategist += 1
            better_player = next_permutation_bot
        
            print("SUPERIOR STRATEGIST FOUND")
            with open('./shared_files/matrixes_that_beat_the_goat.txt', 'a') as file:
                file.write('======================================================================\n')
                file.write('HARD TOTALS:\n')
                file.write(f'{better_player.hard_total_strategy.get_strategy_matrix()}\n')
                file.write('SOFT TOTALS:\n')
                file.write(f'{better_player.soft_total_strategy.get_strategy_matrix()}\n')
                file.write('SPLIT PAIRS:\n')
                file.write(f'{better_player.split_pair_strategy.get_strategy_matrix()}\n')
                file.write('======================================================================\n\n\n')
        
        # Add results to txt file if player beats perfect strategist
        if games_won_by_next_permutation_bot == (best_out_of - 1):
            worthy_competitors += 1
            better_player = next_permutation_bot
        
            print("SUPERIOR STRATEGIST FOUND")
            with open('./shared_files/narrow_defeats.txt', 'a') as file:
                file.write(f'    Perfect Strategist: {games_won_by_perfect_strategist}')
                file.write(f'    Random Strategist: {games_won_by_next_permutation_bot}\n')
                file.write('======================================================================\n')
                file.write('HARD TOTALS:\n')
                file.write(f'{better_player.hard_total_strategy.get_strategy_matrix()}\n')
                file.write('SOFT TOTALS:\n')
                file.write(f'{better_player.soft_total_strategy.get_strategy_matrix()}\n')
                file.write('SPLIT PAIRS:\n')
                file.write(f'{better_player.split_pair_strategy.get_strategy_matrix()}\n')
                file.write('======================================================================\n\n\n')


if __name__ == "__main__":
    start_simulations()