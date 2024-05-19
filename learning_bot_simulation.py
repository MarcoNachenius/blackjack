import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.learning_bot.learning_bot import LearningBot


class LearningBotSimulation(object):
    
    @classmethod
    def start_simulation(cls):
        learner_bot = LearningBot(player_name="Learner Bot", custom_starting_chips=100000)
        game = Game(all_players=[learner_bot])
        while learner_bot.get_chips() > 10:
            # Initiate new round
            game.start_new_round()
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
            # Print statements
            os.system('cls')
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