from blackjack.players.player import Player
from blackjack.card import Card
from blackjack.hand import Hand
from blackjack.print_statements import *

from typing import List

class Human(Player):
    """docstring for Human."""
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
    
    def request_split_pair(self, hand: Hand) -> bool:
        HandStatements.hand_cards_and_points(hand=hand)
        response = input("Split pair? [y/n]\n")
        if response == "y":
            return True
    
    def request_round_participation(self) -> bool:
        # Exceptions
        # Does player have enough chips to bet?
        participation_request = input("Would you like to play the next round? [y/n]\n")
        if participation_request == "y":
            return True
        else:
            return False
    
    def request_bet_amount(self) -> int:
        print(f'Current balance: {self.get_chips()}')
        total_bet_amount = int(input("Enter the amount of chips you would like to bet:\n"))
        return total_bet_amount
    
    def request_hit(self, hand: Hand) -> bool:
        HandStatements.hand_cards_and_points(hand=hand)
        hit_request = input("Would you like to add a card to hand? [y/n]\n")
        if hit_request == "y":
            return True
        return False
    
    def request_double_down(self, hand: Hand):
        HandStatements.hand_cards_and_points(hand=hand)
        double_down = input("Would you like to double down your hand? [y/n]\n")
        if double_down == "y":
            return True
        return False
    
    
    def request_insurance(self) -> bool:
        HandStatements.hand_cards_and_points(hand=self.get_hands()[0])
        insurance_request = input("Would you like to buy insurance? [y/n]\n")
        if insurance_request == "y":
            return True
        return False
