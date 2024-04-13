from blackjack.game_objects.hand import Hand
from blackjack.game_objects.dealer import Dealer
from blackjack.players.player_abc import Player
from blackjack.print_statements import *

from typing import List

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
        if hand.get_final_outcome() != "":
            print(f'Final outcome: {hand.get_final_outcome()}')
        for card in hand.cards:
            print(f'    {card.full_name()}')
        print(f'Highest score: {hand.max_non_bust_score()}')
        print("")
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
        print("")
    
    @classmethod
    def initial_deal_report(cls, dealer_hand: Hand, participating_players: List[Player]):
        """
        Output Example:
        """
        print("Dealer has successfully dealt two cards to all players and itself")
        print("Dealer hand:")
        print(f'    {dealer_hand.get_cards()[0].full_name()}, {dealer_hand.get_cards()[1].full_name()}')
        print("")
        for player in participating_players:
            print(f'{player.get_player_name()} hand:')
            print(f'    {player.get_hands()[0].cards[0].full_name()}, {player.get_hands()[0].cards[1].full_name()}')
            print("")
    
    @classmethod
    def round_completion_results(cls, dealer_hand: Hand, participating_players: List[Player]):
        print("ROUND HAS CONCLUDED")
        print("")
        print("RESULTS:")
        print("Dealer hand:")
        HandStatements.hand_cards_and_points(hand=dealer_hand)
        for player in participating_players:
            print(f'{player.get_player_name()} game report:')
            print(f'Total winnings: {player.get_total_winnings()}')
            print(f'{player.get_player_name()} hands:')
            for hand in player.get_hands():
                HandStatements.hand_cards_and_points(hand=hand)
            print(f'{player.get_player_name()} balance: {player.get_chips()}\n')