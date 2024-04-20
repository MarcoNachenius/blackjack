"""
This program tests random bot strategies against the PerfectStrategist.

If it is kept running, it will only stop once a strategy has been found that beat that of the PerfectStrategist
"""
import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
from blackjack.players.bots.bot_builder import BotBuilder




if __name__ == "__main__":
    
    # PRINT VALUES
    refresh_rate = 100# Game results are printed after specified amount of simulations
    # GAME VALUES
    gamer_per_simulation = 5 # Amount of games should be odd number to avoid ties
    max_number_of_rounds = 100
    rounds_played = 0
    winner = None
    # SIMULATION RESULTS
    total_rounds = 0
    total_games = 0
    total_simulations = 0
    
    player_that_beat_perfect_strategist = None
    while player_that_beat_perfect_strategist is None:
        #print("STARTING NEW SIMULATION")
        #print("=======================\n")
        games_won_by_perfect_strategist = 0
        games_won_by_random_strategist = 0

        total_simulations += 1
        for _ in range(gamer_per_simulation):
            # Create game and player objects
            random_strategist = BotBuilder.return_random_player()
            perfect_strategist = PerfectStrategist()
            game = Game([random_strategist, perfect_strategist])
            # Increase total number of games
            total_games += 1
            premature_game_winner = None # If game ends before max number of round, a winner will be placed here
            while rounds_played != max_number_of_rounds:
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
                # Start new round
                game.start_new_round()
                game.current_round.clear_round_values(dealer=game.get_dealer())
                rounds_played += 1
                total_rounds += 1
            
            # Check for winner when max round amount is reached
            if len(game.current_round.get_participating_players()) == 2:
               if perfect_strategist.get_chips() > random_strategist.get_chips():
                   games_won_by_perfect_strategist += 1
               else:
                   games_won_by_random_strategist += 1
                
                
            #if premature_game_winner is not None:
            #    print(f'    Game successfully completed!')
            #print(f'    Rounds played: {rounds_played}\n')
            rounds_played = 0
        # Print results every 5 times
        if total_simulations == 1 or total_simulations % refresh_rate == 0:
            os.system('cls')
            print(f'SIMULATION REPORT')
            print("=================================")
            print("Final player scores:")
            print(f'    Perfect Strategist: {games_won_by_perfect_strategist}')
            print(f'    Random Strategist: {games_won_by_random_strategist}\n')
            print(f'Total rounds: {total_rounds}')
            print(f'Total games: {total_games}')
            print(f'Total simulations: {total_simulations}')
            print("=================================\n\n")
        
        
        # Check if random bot has beaten perfect strategist
        if games_won_by_random_strategist > games_won_by_perfect_strategist:
            player_that_beat_perfect_strategist = random_strategist
        
            print("SUPERIOR STRATEGIST FOUND")
            with open('matrixes_that_beat_the_goat.txt', 'a') as file:
                file.write('==================================\n')
                file.write('HARD TOTALS:\n')
                file.write(f'{player_that_beat_perfect_strategist.hard_total_strategy.get_strategy_matrix()}\n')
                file.write('SOFT TOTALS:\n')
                file.write(f'{player_that_beat_perfect_strategist.soft_total_strategy.get_strategy_matrix()}\n')
                file.write('SPLIT PAIRS:\n')
                file.write(f'{player_that_beat_perfect_strategist.split_pair_strategy.get_strategy_matrix()}\n')
                file.write('==================================\n\n\n')
            print("\n Matrix successfully added to matrixes_that_beat_the_goat.txt")
            print("\n PLAYER MATRIXES")
            print('==================================\n')
            print('HARD TOTALS:\n')
            print(f'{player_that_beat_perfect_strategist.hard_total_strategy.get_strategy_matrix()}\n')
            print('SOFT TOTALS:\n')
            print(f'{player_that_beat_perfect_strategist.soft_total_strategy.get_strategy_matrix()}\n')
            print('SPLIT PAIRS:\n')
            print(f'{player_that_beat_perfect_strategist.split_pair_strategy.get_strategy_matrix()}\n')
            print('==================================\n\n\n')

