from players.player import Player
from dealer import Dealer
from typing import List
from card import Card
class Round(object):
    """
    """
    def __init__(self, participating_players: List[Player] = None):
        self.participating_players: List[Player] = participating_players or []
        self.end_of_round = False
    
    def award_dealer_bust_wins(self, dealer: Dealer):
        """
        INCOMPLETE!
        """
        for player in self.get_participating_players():
            for hand in player.get_hands():
                if hand.is_busted():
                    pass
    
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
        for player in self.participating_players:
            # Send insurance requests
            if player.is_able_to_insure() and player.request_insurance():
                dealer.insure_player(player=player)
    
    def conclude_insurance_round(self, dealer: Dealer):
        """
        This method should be called when dealer's face down-card is worth 10 points,
        revealing a natural blackjack
        
        Actions:
            - Dealer awards wins, losses and pushed to all players' hands 
        """
        for player in self.participating_players:
            for hand in player.hands:
                # Asses 
                pass
    
    # Getter for participating_players
    def get_participating_players(self) -> List[Player]:
        return self.participating_players

    # Setter for participating_players
    def set_participating_players(self, participating_players: List[Player]):
        if not isinstance(participating_players, list) or not all(isinstance(player, Player) for player in participating_players):
            raise ValueError("participating_players must be a list of Player instances")
        self.participating_players = participating_players

    # Getter for end_of_round
    def get_end_of_round(self) -> bool:
        return self.end_of_round

    # Setter for end_of_round
    def set_end_of_round(self, end_of_round: bool):
        if not isinstance(end_of_round, bool):
            raise ValueError("end_of_round must be a boolean value")
        self.end_of_round = end_of_round