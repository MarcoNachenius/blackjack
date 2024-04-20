from blackjack.players.player_abc import Player
from blackjack.game_objects.dealer import Dealer
from blackjack.game_objects.hand import Hand
from blackjack.game_objects.card import Card
from blackjack import constants
from typing import List

import math
class Round(object):
    """
    """
    def __init__(self, round_id: int = 0, participating_players: List[Player] = None):
        self.participating_players: List[Player] = participating_players or []
        self.end_of_round = False
        self.round_id: int = round_id
        
    
    def clear_round_values(self, dealer: Dealer):
        """
        Clears all values for players and the dealer that have to do with the current round.
        """
        # Clear dealer hand
        dealer.set_hand(Hand())
        dealer.set_hand_id(0)
        # Clear player values
        for player in self.get_participating_players():
            player.set_initial_bet_amount(0)
            player.set_is_insured(False)
            player.set_total_bet_amount(0)
            player.set_hands([Hand()])
            player.set_total_winnings(0)
            player.set_hand_combo_id(0)
        return
            
    def award_dealer_bust_wins(self, dealer: Dealer):
        """
        docstring
        """
        print("DEALER BUST\n")
        for player in self.get_participating_players():
            for hand in player.get_hands():
                if hand.max_non_bust_score() != 0:
                    dealer.award_win(hand=hand, player=player)
    
    def send_bet_requests(self, all_players: List[Player], dealer: Dealer, print_log: bool =False):
        """
        Populates self.participating_players list.
        If  player is added to list, it means that initial bet has\n
        also been successfully placed.\n
        \n
        Player is only sent request if:\n
        - Player has more than 0 chips\n
        """
        for player in all_players:
            if print_log:
                print(f'Taking bet from {player.get_player_name()}')
            # Check player balance
            if not player.has_enough_to_bet():
                #self.set_participating_players(self.get_participating_players().remove(player))
                continue
            # Get bet amount from player
            bet_amount = player.request_bet_amount()
            if bet_amount < constants.MIN_BET_AMOUNT:
                #self.set_participating_players(self.get_participating_players().remove(player))
                continue
            if bet_amount > player.get_chips():
                continue
            # Assumes player has placed valid bet amount
            player.hands[0].set_active(True)
            player.set_initial_bet_amount(bet_amount)
            dealer.accept_player_bet(bet_amount=bet_amount, hand=player.get_hands()[0], player=player)
            self.participating_players.append(player)
            player.subtract_from_total_winnings(bet_amount)

    def send_hit_request(self, dealer: Dealer, table_deck: List[Card], player: Player, hand: Hand):
        if not hand.is_active():
            return
        while hand.is_busted() == False and hand.is_active():
            if player.request_hit(hand=hand, dealer_upcard=dealer.get_hand().get_cards()[0]):
                dealer.hit_player_hand(hand=hand, table_deck=table_deck)
            else:
                hand.set_active(False)
        return
    
    def send_split_request(self, dealer: Dealer, table_deck: List[Card], player: Player, hand: Hand):
        """
        Sends split request for hand to player if:\n
        - Player has pair\n
        - Player has less than max allowed hands\n
        - Player has enough chips to split hand\n
        """
        while hand.is_splittable() and player.is_able_to_split() and not hand.get_rejected_split_request():
            # Send split request to player
            if player.request_split_pair(hand=hand, dealer_upcard = dealer.get_hand().get_cards()[0]):
                dealer.split_player_hand(split_hand=hand, player=player, table_deck=table_deck)
            else: 
                hand.set_rejected_split_request(True)
        return
                
    def send_double_down_request(self, dealer: Dealer, table_deck: List[Card], player: Player, hand: Hand):
        if not player.is_able_to_double_down():
            return
        if player.request_double_down(hand=hand, dealer_upcard = dealer.get_hand().get_cards()[0]):
            dealer.double_down_player_hand(player_hand=hand, player=player, table_deck=table_deck)
        return
    
    def award_wins_comparatively(self, dealer: Dealer, print_results: bool = False):
        for player in self.get_participating_players():
            for hand in player.get_hands():
                # Check for natural blackjack
                if hand.has_natural_blackjack():
                    dealer.award_natural_blackjack_win(hand=hand, player=player)
                    continue
                # Check for bust
                if hand.max_non_bust_score() == 0:
                    if print_results:
                        print("BUST LOSS\n")
                        print(f'{player.get_player_name()} has lost {hand.current_bet_amount()} chips')
                    continue
                # Check for same score as dealer
                if hand.max_non_bust_score() == dealer.hand.max_non_bust_score():
                    dealer.award_push(hand=hand, player=player)
                    continue
                # Check for higher score than dealer
                if hand.max_non_bust_score() > dealer.hand.max_non_bust_score():
                    dealer.award_win(hand=hand, player=player)
                    continue
                if print_results:
                    print("AWARDED LOSS\n")
                    print(f'{player.get_player_name()} has lost bet of {hand.current_bet_amount()} chips')
                hand.set_final_outcome("LOSS")
        return
    
    def send_insurance_requests(self, dealer: Dealer):
        """
        Sends insurance and even money requests to players whenever applicable
        
        If the dealer has an Ace or a tem-point card:
            - Send even money requests to players that have natural blackjack
            - Send insurance requests to players that don't have natural blackjack
        """
        for player in self.participating_players:
            # Send insurance requests
            if player.is_able_to_insure() and player.request_insurance(hand=player.get_hands()[0], dealer_upcard=dealer.get_hand().get_cards()[0]):
                dealer.insure_player(player=player)
    
    def conclude_insurance_round(self, dealer: Dealer):
        """
        This method should be called when dealer's face down-card is worth 10 points,
        revealing a natural blackjack
        
        Actions:
            - Dealer awards wins, losses and pushed to all players' hands 
        """
        for player in self.get_participating_players():
            for hand in player.get_hands():
                # Check for player natural blackjack
                if hand.has_natural_blackjack():
                    if player.get_is_insured():
                        player.add_chips(player.get_initial_bet_amount())
                        player.add_to_total_winnings(player.get_initial_bet_amount())
                    player.add_chips(player.get_initial_bet_amount())
                    player.add_to_total_winnings(player.get_initial_bet_amount())
                    hand.set_final_outcome("PUSH")
                    continue
                hand.set_final_outcome("LOSS")               
        return
                    
    
    # Getter for participating_players
    def get_participating_players(self) -> List[Player]:
        return self.participating_players

    # Setter for participating_players
    def set_participating_players(self, participating_players: List[Player]):
        if not isinstance(participating_players, list) or not all(isinstance(player, Player) for player in participating_players):
            raise ValueError("participating_players must be a list of Player instances\n")
        self.participating_players = participating_players

    # END_OF_ROUND
    def get_end_of_round(self) -> bool:
        return self.end_of_round
    def set_end_of_round(self, end_of_round: bool):
        if not isinstance(end_of_round, bool):
            raise ValueError("end_of_round must be a boolean value\n")
        self.end_of_round = end_of_round
    
    # ROUND_ID
    def get_round_id(self) -> int:
        return self.round_id
    def set_round_id(self, round_id: int):
        if not isinstance(round_id, int):
            raise ValueError("round_id must be a int value\n")
        self.round_id = round_id