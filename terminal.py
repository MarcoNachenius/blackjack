from dealer import Dealer
from typing import List
from player import Player
class Terminal(object):
    """
    The Terminal class controls the display of all multi-line displays 
    """
    def print_round_status(self, dealer: Dealer, participating_players: List[Player]):
        """
        Prints the following information:
            - Dealer
                - Dealer hand
            - Players
                - Player name
                - Player hands
                    - Cards
                    - Bet amount
        """
        print("Current round status:")
        print("===============\n")
        print("Dealer:")
        print("-------\n")
        print(" - Cards:")
        for card in dealer.hand.cards:
            if card.visible is False:
                print("     - Hidden")
                continue    
            print(f'     - {card.full_name}')
        print("\nPlayers:")
        print("--------\n")
        for player in participating_players:
            print(f'Player: {player.player_name}')
            print(" - Hands:")
            for hand in player.hands:
                print()