import time
from blackjack.strategy_manager.strategy_matrixes.soft_totals import SoftTotalStrategy
from blackjack.strategy_manager.strategy_matrixes.hard_totals import HardTotalStrategy
import numpy as np

from blackjack.players.bots.bot_builder import BotBuilder
from blackjack.players.bots.strategist_abc import Strategist

player = Strategist(player_name="Yo")

with open('./superior_matrixes/matrixes_that_beat_the_goat.txt', 'a') as file:
                file.write('==================================\n')
                file.write('HARD TOTALS:\n')