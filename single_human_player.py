from game import Game
from players.human import Human
from players.bots.yesman import Yesman
from constants import *

if __name__ == "__main__":
    all_players = [Human(player_name="Foo")]
    game = Game(all_players=all_players)
    game.start_new_round()
    another_round_request = input("Play another round? [y/n]")
    while another_round_request == "y":
        game.start_new_round()
        another_round_request = input("Play another round? [y/n]")
    