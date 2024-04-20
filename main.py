import time
from blackjack.strategy_manager.strategy_matrixes.soft_totals import SoftTotalStrategy
from blackjack.strategy_manager.strategy_matrixes.hard_totals import HardTotalStrategy
import numpy as np

from blackjack.players.bots.bot_builder import BotBuilder
from blackjack.players.bots.strategist_abc import Strategist

player = Strategist(player_name="Yo")

for _ in range(4):
    player = BotBuilder.return_random_player()
    with open('matrixes_that_beat_the_goat.txt', 'a') as file:
        file.write('==================================\n')
        file.write('HARD TOTALS:\n')
        file.write(f'{player.hard_total_strategy.get_strategy_matrix()}\n')
        file.write('SOFT TOTALS:\n')
        file.write(f'{player.soft_total_strategy.get_strategy_matrix()}\n')
        file.write('SPLIT PAIRS:\n')
        file.write(f'{player.split_pair_strategy.get_strategy_matrix()}\n')
        file.write('==================================\n\n\n')