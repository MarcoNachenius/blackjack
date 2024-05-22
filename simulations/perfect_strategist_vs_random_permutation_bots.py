"""
This program tests random bot strategies against the PerfectStrategist.

Rules
- Every player has the same number of chips at the start of every game
- The first player to win a certain number of games is the winner
- A game is won when one of the players goes broke, or when one of the players has the most chips within a maximum number of rounds.
"""
import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
from blackjack.players.bots.bot_builder import BotBuilder




if __name__ == "__main__":
    with open('./shared_files/container_logs.txt', 'a') as file:
                file.write("ps vs random permutational strategy bots container added\n")
    # Generate bot with random strategy matrixes
    random_bot = BotBuilder.return_random_player()
    
    # PRINT VALUES
    refresh_rate = 1# Game results are printed after specified amount of simulations
    # GAME VALUES
    best_out_of = 7 # Amount of games should be odd number to avoid ties
    max_number_of_rounds = 200
    rounds_played = 0
    winner = None
    # SIMULATION RESULTS
    total_rounds = 0
    total_games = 0
    total_simulations = 0
    
    players_that_beat_perfect_strategist = 0
    worthy_competitors = 0
    
    last_ht_matrix = None
    last_st_matrix = None
    last_sp_matrix = None
    
    while True:
        games_won_by_perfect_strategist = 0
        games_won_by_random_strategist = 0
        # Increase simulation number
        total_simulations += 1
        while games_won_by_perfect_strategist < best_out_of and  games_won_by_random_strategist < best_out_of:
            # Create game and player objects
            random_strategist = BotBuilder.return_next_permutation_player(random_bot)
            random_bot = random_strategist
            perfect_strategist = PerfectStrategist()
            last_ht_matrix = random_strategist.hard_total_strategy.get_strategy_matrix()
            last_st_matrix = random_strategist.soft_total_strategy.get_strategy_matrix()
            last_sp_matrix = random_strategist.split_pair_strategy.get_strategy_matrix()
            game = Game([random_strategist, perfect_strategist])
            # Increase total number of games
            total_games += 1
            premature_game_winner = None # If game ends before max number of round, a winner will be placed here
            
            while rounds_played != max_number_of_rounds:
                # Start new round
                game.start_new_round()
                # Check for round limit
                rounds_played += 1
                total_rounds += 1
                # Check for winner
                if len(game.current_round.get_participating_players()) == 1:
                    premature_game_winner = game.current_round.get_participating_players()[0]
                    #print(f'    Game successfully completed!')
                    #print(f'    {premature_game_winner.get_player_name()} has won the game')
                    if premature_game_winner.get_player_name() == "Perfect Strategist":
                        games_won_by_perfect_strategist += 1
                    else:
                        games_won_by_random_strategist += 1
                    break
                
                if rounds_played < max_number_of_rounds:
                    game.current_round.clear_round_values(dealer=game.get_dealer())
            
            # Check for winner when max round amount is reached
            if len(game.current_round.get_participating_players()) == 2:
                if perfect_strategist.get_chips() > random_strategist.get_chips():
                    games_won_by_perfect_strategist += 1
                else:
                    games_won_by_random_strategist += 1
                
                
            rounds_played = 0
        # Print results every 5 times
        if total_simulations == 1 or total_simulations % refresh_rate == 0:
            os.system('clear')
            print("*********************************************************************")
            print("         PERFECT STRATEGIST VS RANDOM BOTS")
            print("*********************************************************************\n")
            print(f'RESULTS FOR SIMULATION {total_simulations}')
            print("=====================================================================")
            print("Player scores:")
            print(f'    Perfect Strategist: {games_won_by_perfect_strategist}')
            print(f'    Random Strategist: {games_won_by_random_strategist}\n')
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
        if games_won_by_random_strategist > games_won_by_perfect_strategist:
            players_that_beat_perfect_strategist += 1
            better_player = random_strategist
        
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
        if games_won_by_random_strategist == (best_out_of - 1):
            worthy_competitors += 1
            better_player = random_strategist
        
            print("SUPERIOR STRATEGIST FOUND")
            with open('./shared_files/narrow_defeats.txt', 'a') as file:
                file.write(f'    Perfect Strategist: {games_won_by_perfect_strategist}')
                file.write(f'    Random Strategist: {games_won_by_random_strategist}\n')
                file.write('======================================================================\n')
                file.write('HARD TOTALS:\n')
                file.write(f'{better_player.hard_total_strategy.get_strategy_matrix()}\n')
                file.write('SOFT TOTALS:\n')
                file.write(f'{better_player.soft_total_strategy.get_strategy_matrix()}\n')
                file.write('SPLIT PAIRS:\n')
                file.write(f'{better_player.split_pair_strategy.get_strategy_matrix()}\n')
                file.write('======================================================================\n\n\n')
