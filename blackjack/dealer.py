from blackjack.card import Card
from blackjack.hand import Hand
from blackjack.players.player import Player
from blackjack.hand import Hand
import blackjack.constants

from typing import List
import random
import math

class Dealer(object):
    """
    The dealer is the sole owner and controller of the table deck.
    """
    def __init__(self, starting_hand: Hand = None):
        self.hand: Hand = starting_hand or Hand()
    
    def get_hand(self) -> Hand:
        return self.hand
    
    def set_hand(self, hand: Hand):
        self.hand = hand
        return
    
    def accept_player_bet(self, bet_amount: int, hand: Hand, player: Player):
        """
        Subtracts bet amount from player balance and adds it to 
        bet amount for hand
        """
        player.subtract_chips(bet_amount)
        hand.set_amount_betted(bet_amount)
        hand.set_active(True)
    
    def deal_card(self, player_hand: Hand, table_deck: List[Card], hide_card = False, deal_next_card = False):
        """
        The Dealer removes a random card from the table deck and adds it to a player's hand. \n
        By default, the dealer places the card in the player's starting hand(in the case of a split).
        """
        if deal_next_card:
            random_card = table_deck.pop(0)
        else:
            # Randomly select a card from the table deck
            random_card = random.choice(table_deck)
        # Check if card should be hidden
        if not hide_card:
            random_card.make_visible()
        # Add the randomly selected card to the player's hand
        player_hand.add_card(random_card)
        # Remove the card from the table deck
        if not deal_next_card:
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
            split_hand.set_rejected_split_request(True)
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
        player.subtract_chips(player.get_initial_bet_amount())
        new_hand.set_amount_betted(player.get_initial_bet_amount())
        player.subtract_from_total_winnings(player.get_initial_bet_amount())
        return
    
    def award_natural_blackjack_win( self, hand: Hand, player: Player):
        """
        Transfers winning amount to player's chips
        
        Awards player 3:2 win.\n
        Assumes player has natural blackjack\n
        If player is awarded an amount of chips that is not a whole number, the amount will be floored(rounded down). 
        """
        print("NATURAL BLACKJACK WIN")
        print(f'{player.get_player_name()} has won {int(math.floor(hand.get_amount_betted() * 1.5))} chips')
        hand.set_final_outcome("WIN")
        total_winnings = math.floor(hand.get_amount_betted() * 2.5)
        player.add_chips(total_winnings)
        player.add_to_total_winnings(total_winnings)
        hand.deactivate()
    
    
    def award_push(self, hand: Hand, player: Player):
        """
        Adds bet amount to 
        """
        push_amount = hand.current_bet_amount()
        player.add_chips(push_amount)
        player.add_to_total_winnings(push_amount)
        hand.set_final_outcome("PUSH")
        print("PUSH")
        print(f'{player.get_player_name()} has been awarded a push')
        return
    
    def needs_to_hit_again(self, participating_players: List[Player]) -> bool:
        """
        Returns False if the dealer is already has a hand that will beat all
        of the other hans on the table
        """
        # Check for dealer hand bust
        if self.hand.max_non_bust_score() == 0:
            return False
        # Check for dealer hand hit limit
        if self.hand.max_non_bust_score() >= constants.DEALER_HIT_LIMIT:
            return False
        # Verify if all hands are bust
        all_hands_bust = True
        # Compare dealer hand to every other hand in play
        for player in participating_players:
            for hand in player.hands:
                # Skip bust hands
                if hand.max_non_bust_score() == 0:
                    continue
                # Check if non-bust hand has been found
                if all_hands_bust and hand.max_non_bust_score() != 0:
                    all_hands_bust = False
                # Check if player hand has higher score than dealer hand
                if hand.max_non_bust_score() >= self.hand.max_non_bust_score():
                    return True
                    
        return all_hands_bust
    
    def award_win(self, hand: Hand, player: Player):
        """
        Adds twice the bet amount to player chips
        """
        print("WIN")
        print(f'{player.get_player_name()} has won {hand.current_bet_amount()} chips')
        total_winnings = hand.current_bet_amount() * 2
        player.add_chips(total_winnings)
        player.add_to_total_winnings(total_winnings)
        hand.set_final_outcome("WIN")
    
    def insure_player(self, player: Player):
        """
        Requests if a player wants to insure hand.
        If player accepts request, insurance status is turned on (player.is_insured=True)
        """
        player.set_is_insured(True)
        insurance_amount = math.ceil(player.get_initial_bet_amount()*0.5)
        player.subtract_chips(insurance_amount)
        player.subtract_from_total_winnings(insurance_amount)
        return
    
    def hit_player_hand(self, hand: Hand, table_deck: List[Card]):
        """
        Add card to player hand\n
        If player hand is bust:
            - Bust status adjusted
            - Hand deactivated
        """
        self.deal_card(player_hand=hand, table_deck=table_deck)
        if hand.lowest_score() > 21:
            hand.set_busted()
            hand.deactivate()
    
    def double_down_player_hand(self, player_hand: Hand, player: Player, table_deck: List[Card]):
        """
        Does
        - Changes double down status
        - Removes chips from player
        todo:
        - Check if hand is in player_hand
        """
        player_hand.set_doubled_down(True)
        player_hand.set_active(False)
        self.deal_card(player_hand=player_hand, table_deck=table_deck)
        player.subtract_chips(player.get_initial_bet_amount())
        player.subtract_from_total_winnings(player.get_initial_bet_amount())
        
    
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
    