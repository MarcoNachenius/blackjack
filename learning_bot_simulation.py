import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.learning_bot.learning_bot import LearningBot
from blackjack.database_manager.lerner_bot_database.learner_bot_db_builder import LearningBotDbBuilder
from blackjack.database_manager.lerner_bot_database.learner_bot_db_setters import LearningBotDbSetters


class LearningBotSimulation(object):
    
    DATABASE_UPDATE_RATE = 10
    PRINT_STATUS_REFRESH_RATE = 100
    @classmethod
    def start_simulation(cls, db_path):
        # Create database if it does not exist
        if not os.path.isfile(db_path):
            LearningBotDbBuilder.create_learner_bot_database(db_path)
            
        # Track number of rounds played
        total_rounds = 0
        
        # Initiate bot and game objects
        learner_bot = LearningBot(player_name="Learner Bot", custom_starting_chips=100000)
        game = Game(all_players=[learner_bot])
        
        # Start simulations
        while learner_bot.get_chips() > 10:
            # Initiate new round
            game.start_new_round()
            # Increase number of rounds 
            total_rounds += 1
            # Process player round logs
            learner_bot.process_all_round_logs(total_winnings=learner_bot.get_total_winnings())
            # Increment all action numbers that have been used
            learner_bot.increment_strategy_matrix_action_numbers()
            # Clear learner bot round logs
            learner_bot.clear_round_logs()
            # Clear round values for player and dealer
            game.current_round.clear_round_values(dealer=game.get_dealer())
            # Reset player balance to allow for infinite sunning of simulation
            learner_bot.set_chips(1000)
            
            if total_rounds % cls.DATABASE_UPDATE_RATE == 0:
                # Update HardTotalsMemory table
                LearningBotDbSetters.increase_hard_totals_memory_trials_and_points(db_path=db_path, hard_total_memory_strategy=learner_bot.lb_hard_total_memory_matrix)
                learner_bot.clear_lb_hard_total_memory_matrix()
                # Update SoftTotalsMemory table
                LearningBotDbSetters.increase_soft_totals_memory_trials_and_points(db_path=db_path, soft_total_memory_strategy=learner_bot.lb_soft_total_memory_matrix)
                learner_bot.clear_lb_soft_total_memory_matrix()
                # Update SplitPairsMemory table
                LearningBotDbSetters.increase_split_pairs_memory_trials_and_points(db_path=db_path, split_pair_memory_strategy=learner_bot.lb_split_pair_memory_matrix)
                learner_bot.clear_lb_split_pair_memory_matrix()
            
            # Print statements
            os.system('cls')
            print("BEST PERFORMING STRATEGIES")
            print(f'  SOFT TOTAL MATRIX       HARD TOTAL MATRIX       SPLIT PAIR MATRIX')
            for i in range(len(learner_bot.soft_total_strategy.get_strategy_matrix())):
                if i < 10:
                    print(f'{learner_bot.soft_total_strategy.get_strategy_matrix()[i]}   {learner_bot.hard_total_strategy.get_strategy_matrix()[i]}   {learner_bot.split_pair_strategy.get_strategy_matrix()[i]}')
                    continue
                if i < 18:
                    print(f'{learner_bot.soft_total_strategy.get_strategy_matrix()[i]}   {learner_bot.hard_total_strategy.get_strategy_matrix()[i]}')
                    continue
                print(f'{learner_bot.soft_total_strategy.get_strategy_matrix()[i]}')
    
if __name__ == "__main__":
    LearningBotSimulation.start_simulation()