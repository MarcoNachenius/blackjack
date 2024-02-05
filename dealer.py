from card import Card
from hand import Hand
from player import Player

from typing import List
import random
import math

class Dealer(object):
    """
    When a Dealer object is created, the starting table deck is also created.\n
    The dealer is the sole owner and controller of the table deck.\n
    \n
    """
    def __init__(self, starting_hand: Hand = None):
        """
        self.starting_deck is populated by default with constants.Deck.starting_deck(), but can be adjusted 
        """
        self.hand: Hand = starting_hand or Hand()
    
    def deal_card(self, player_hand: Hand, table_deck: List[Card], hide_card = False):
        """
        The Dealer removes a random card from the table deck and adds it to a player's hand. \n
        By default, the dealer places the card in the player's starting hand(in the case of a split).
        """
        # Randomly select a card from the table deck
        random_card = random.choice(table_deck)
        # Check if card should be hidden
        if not hide_card:
            random_card.make_visible()
        # Add the randomly selected card to the player's hand
        player_hand.add_card(random_card)
        # Remove the card from the table deck
        table_deck.remove(random_card)
        return
    
    def split_player_hand(self, split_hand: Hand, player: Player, table_deck: List[Card]):
        """
        This function should only be called after a player has accepted the request_split_pair request
        
        Does:
        - Split player hand and deal new card for both hands
        - Remove chips from player balance
        - Chang player insurance status
        todo:
        - Check if split_hand is in player_hand
        """
        # Skip method if player does not have a pair
        if not split_hand.is_splittable():
            return
        # Create new hand
        # First card of new hand is second card of split_hand
        new_hand = Hand(first_card=split_hand.cards.pop(1))
        # Add hand to player hands
        player.hands.append(new_hand)
        # Deals cards for split hand and and new hand
        self.deal_card(player_hand=split_hand, table_deck=table_deck)
        self.deal_card(player_hand=new_hand, table_deck=table_deck)
        # Subtract bet amount from player
        player.chips -= player.initial_bet_amount
    
    def award_natural_blackjack_win( self, player: Player):
        """
        Transfers winning amount to player's chips
        
        Awards player 3:2 win.\n
        Assumes player has natural blackjack\n
        If player is awarded an amount of chips that is not a whole number, the amount will be floored(rounded down). 
        """
        player_win_amount = player.initial_bet_amount
        if player.is_insured:
            player_win_amount /= 2
        player.add_chips(math.floor(player_win_amount * 1.5) + player_win_amount)
    
    def insure_player(self, player: Player):
        """
        Requests if a player wants to insure hand.
        If player accepts request, insurance status is turned on (player.is_insured=True)
        """
        if player.request_insurance():
            # Change player insurance status
            player.is_insured = True
    
    def hit_player_hand(self, hand: Hand, player: Player):
        """
        5.1.1 Hit:
            5.1.1.1 Player takes an additional card to increase their hand total.
            5.1.1.2 Repeat until the player stands or busts (hand value over 21).
        """
        pass
    
    def double_down_player_hand(self, hand: Hand, player: Player, table_deck: List[Card]):
        """
        Does
        - Changes double down status
        - Removes chips from player
        todo:
        - Check if hand is in player_hand
        """
        hand.doubled_down = True
        hand.active = False
        self.deal_card(player_hand=hand, table_deck=table_deck)
        player.chips -= player.initial_bet_amount
        
    
    def deal_initial_cards(self, table_deck: List[Card], participating_players: List[Player]):
        """
        Fulfills the following steps of the game: 
        2. Initial Deal:
            2.1 Dealer deals two cards for every player who has placed a bet.
            2.3 Dealer deals two cards for themselves, one face-up and one face-down.
        """
        # 1.1 Dealer takes bets from players at the table.
        for player in participating_players:
            self.deal_card(table_deck=table_deck, player_hand=player.hands[0])
            self.deal_card(table_deck=table_deck, player_hand=player.hands[0])
        # 2.2 Dealer deals two cards for themselves, one face-up and one face-down
        self.deal_card(table_deck=table_deck, player_hand=self.hand)
        self.deal_card(table_deck=table_deck, player_hand=self.hand, hide_card=True)