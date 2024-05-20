from learning_bot_simulation import LearningBotSimulation
from blackjack.database_manager.lerner_bot_database.learner_bot_db_getters import LearningBotDbGetters
import os

db_path = 'test_lb.db'
#LearningBotSimulation.start_simulation(db_path)
#os.remove(db_path)

results = LearningBotDbGetters.get_next_hard_totals_matrix_to_test(db_path)
print(results)