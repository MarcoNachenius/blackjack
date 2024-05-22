import os

from blackjack.game_objects.game import Game
from blackjack.players.bots.learning_bot.learning_bot import LearningBot
from blackjack.database_manager.lerner_bot_database.learner_bot_db_builder import LearningBotDbBuilder
from blackjack.database_manager.lerner_bot_database.learner_bot_db_setters import LearningBotDbSetters
from blackjack.database_manager.lerner_bot_database.learner_bot_db_getters import LearningBotDbGetters


class LearningBotSimulation(object):
    
    HARD_AND_SOFT_TOTAL_ACTION_NUMBERS = [
        "0 = Stand / Don't split pair",
        "1 = Hit / Split pair",
        "2 = Double down, hit",
        "3 = Double down, stand",
        "4 = Buy insurance, hit",
        "5 = Buy insurance, stand",
        "6 = Buy insurance, double down, hit",
        "7 = Buy insurance, double down, stand",
        "",
        ""
    ]
    
    DATABASE_UPDATE_RATE = 1000
    HT_INDEX_TO_PS = LearningBotDbSetters.HARD_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE
    ST_INDEX_TO_PS = LearningBotDbSetters.SOFT_TOTAL_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE
    SP_INDEX_TO_PS = LearningBotDbSetters.SPLIT_PAIR_MATRIX_INDEX_NUMBER_TO_PLAYER_SCORE

    @classmethod
    def start_simulation(cls, db_path):
        # Create database if it does not exist
        if not os.path.isfile(db_path):
            LearningBotDbBuilder.create_learner_bot_database(db_path)
        # Track number of rounds played
        total_rounds = 0
        while True:
            # Initiate bot and game objects
            learner_bot = LearningBot(player_name="Learner Bot")
            game = Game(all_players=[learner_bot])

            # populate leaner bot strategy matrixes with values from database
            learner_bot.hard_total_strategy.set_strategy_matrix(LearningBotDbGetters.get_next_hard_totals_matrix_to_test(db_path))
            learner_bot.soft_total_strategy.set_strategy_matrix(LearningBotDbGetters.get_next_soft_totals_matrix_to_test(db_path))
            learner_bot.split_pair_strategy.set_strategy_matrix(LearningBotDbGetters.get_next_split_pairs_matrix_to_test(db_path))

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

                if total_rounds % cls.DATABASE_UPDATE_RATE == 1:
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
                    ideal_soft_total_matrix = LearningBotDbGetters.get_ideal_soft_total_matrix(db_path)
                    ideal_hard_total_matrix = LearningBotDbGetters.get_ideal_hard_total_matrix(db_path)
                    ideal_split_pair_matrix = LearningBotDbGetters.get_ideal_split_pair_matrix(db_path)
                    print_statement = ""
                    print_statement += ("                         ==========================                     \n")
                    print_statement += ("                         BEST PERFORMING STRATEGIES                     \n")
                    print_statement += ("                         ==========================                     \n")
                    print_statement += ("                                                                        \n")
                    print_statement += ("    SOFT TOTAL MATRIX         HARD TOTAL MATRIX         SPLIT PAIR MATRIX  \n")
                    print_statement += ("                                                                     \n")
                    print_statement += ("  |A|2|3|4|5|6|7|8|9|T|     |A|2|3|4|5|6|7|8|9|T|     |A|2|3|4|5|6|7|8|9|T|\n")
                    for i in range(20):
                        if i < 18:
                            ht_act_num = cls.HT_INDEX_TO_PS[i]
                            ht_act_num = f" {str(ht_act_num)}" if ht_act_num < 10 else str(ht_act_num)
                        st_act_num = cls.ST_INDEX_TO_PS[i]
                        st_act_num = f" {str(st_act_num)}" if st_act_num < 10 else str(st_act_num)
                        if i < 10:
                            sp_act_num = cls.SP_INDEX_TO_PS[i]
                            sp_act_num = f" {str(sp_act_num)}" if sp_act_num < 10 else str(sp_act_num)
                        if i < 10:
                            print_statement += (f'{st_act_num}{ideal_soft_total_matrix[i]}   {ht_act_num}{ideal_hard_total_matrix[i]}   {sp_act_num}{ideal_split_pair_matrix[i]}       {cls.HARD_AND_SOFT_TOTAL_ACTION_NUMBERS[i]}\n')
                            continue
                        if i < 18:
                            print_statement += (f'{st_act_num}{ideal_soft_total_matrix[i]}   {ht_act_num}{ideal_hard_total_matrix[i]}\n')
                            continue
                        print_statement += (f'{st_act_num}{ideal_soft_total_matrix[i]}\n')
                    os.system('clear')
                    print(print_statement)
    
