from game import Game
from players.human import Human
from constants import *

if __name__ == "__main__":
    all_players = [Human(player_name="Marco")]
    game = Game(all_players=all_players)
    game.start_new_round()