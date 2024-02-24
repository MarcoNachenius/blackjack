from hand import Hand
from dealer import Dealer
from typing import List
from players.player import Player
from print_statements import *

class HandStatements(object):
    """
    Dea
    """
    @classmethod
    def hand_cards_and_points(cls, hand: Hand):
        """
        Example: \n
        Hand:
            Eight of Clubs
            Jack of Hearts
        Highest score: 18
        """
        print("Hand:")
        for card in hand.cards:
            print(f'    {card.full_name()}')
        print(f'Highest score: {hand.max_non_bust_score()}')
        return 
class RoundStatements(object):
    """
    PrintStatement is a method class that functions as a repository for all print statements
    that will be used frequently. The purpose of this class is to reduce the need for repetitive boilerplate
    code, and to set a unifying standard format   
    """
    @classmethod
    def successful_bet_placed(cls, player: Player):
        """
        Output example: \n
        "Zack has successfully placed a bet of 100 chips"
        """
        print(f'{player.get_player_name()} has successfully placed a bet of {str(player.get_initial_bet_amount())} chips')
    
    @classmethod
    def initial_deal_report(cls, dealer_hand: Hand, participating_players: List[Player]):
        """
        Output Example:
        """
        print("Dealer has successfully dealt two cards to all players and itself")
        print("Dealer hand:")
        print(f'    {dealer_hand.get_cards()[0].full_name()}, Face-down card')
        for player in participating_players:
            print(f'{player.get_player_name()} hand:')
            print(f'    {player.get_hands()[0].cards[0].full_name()}, {player.get_hands()[0].cards[1].full_name()}')
    
    @classmethod
    def round_completion_results(cls, dealer_hand: Hand, participating_players: List[Player]):
        print("ROUND HAS CONCLUDED")
        print("RESULTS:")
        print("Dealer hand:")
        HandStatements.hand_cards_and_points(hand=dealer_hand)
        for player in participating_players:
            print(f'{player.get_player_name()} hands:')
            for hand in player.get_hands():
                HandStatements.hand_cards_and_points(hand=hand)
            print(f'{player.get_player_name()} balance: {player.get_chips()}')