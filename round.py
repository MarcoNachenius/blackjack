from player import Player
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
                while hand.is_splittable() and player.is_able_to_split():
                    # Send split request to player
                    if player.request_split_pair():
                        dealer.split_player_hand(split_hand=hand, player=player, table_deck=table_deck)
                
    def send_double_down_requests(self):
        pass
    
    
    def send_insurance_requests(self):
        pass
    
    def award_natural_blackjack_wins(self, dealer: Dealer, participating_players: List[Player]):
        """
        Fulfills following steps of round: \n
        - 4. Check for Player Blackjack:
            - 4.1 If any player has a natural blackjack, pay them 3:2 on their bet.
            - 4.2 Remove player from round's participating players list
        """
        for player in participating_players:
            if player.hands[0].has_natural_blackjack:
                # Step 4.1
                dealer.award_natural_blackjack_win(player=player)
                # Step 4.2
                participating_players.remove(player)