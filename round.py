from players.player import Player
from dealer import Dealer
import constants
from typing import List
from card import Card
class Round(object):
    """
    """
    def __init__(self, participating_players: List[Player] = None):
        self.participating_players: List[Player] = participating_players or []
        self.end_of_round = False
    
        
    
    def send_bet_requests(self, all_players: List[Player]):
        """
        Populates self.participating_players list.
        If  player is added to list, it means that initial bet has\n
        also been successfully placed.\n
        \n
        Player is only sent request if:\n
        - Player has more than 0 chips\n
        """
        for player in all_players:
            if player.request_bet_amount > 0:
                self.participating_players.append(player)
    
    def send_split_requests(self, dealer: Dealer, table_deck: List[Card]):
        """
        Requests are only sent to player if:\n
        - Player has pair\n
        - Player has less than max allowed hands\n
        - Player has enough chips to split hand\n
        """
        for player in self.participating_players:
            
            # Dealer only sends split request if hand has pair and player has less than max
            # allowed number of hands
            for hand in player.hands:
                if hand.rejected_split_request:
                    continue
                while hand.is_splittable() and player.is_able_to_split() and not hand.rejected_split_request:
                    # Send split request to player
                    if player.request_split_pair():
                        dealer.split_player_hand(split_hand=hand, player=player, table_deck=table_deck)
                    else: 
                        hand.reject_split_request()
                
    def send_double_down_requests(self):
        pass
    
    
    def send_insurance_requests(self, dealer: Dealer):
        """
        Sends insurance and even money requests to players whenever applicable
        
        If the dealer has an Ace or a tem-point card:
            - Send even money requests to players that have natural blackjack
            - Send insurance requests to players that don't have natural blackjack
        """
        if dealer.hand[0].rank == "Ace" or dealer.hand[0].points == 10:
            for player in self.participating_players:
                # Send insurance requests
                if player.request_insurance():
                    dealer.insure_player(player=player)
