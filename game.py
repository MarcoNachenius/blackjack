from players.player import Player
from dealer import Dealer
from round import Round
from card import Card
from constants import Deck

from typing import List

class Game(object):
    """
    When the game object is initiated
    
    Table deck is loaded to 
    """
    def __init__(self, all_players: List[Player] = None, starting_deck: List[Card] = None):
        self.dealer: Dealer = Dealer()
        self.all_players: List[Player] = all_players
        self.in_progress = True
        self.current_round: Round = None
        self.table_deck = starting_deck or Deck.starting_deck()
    
    def start_game(self):
        # Exceptions
        # - Has the game been loaded with a dealer and players?
        
        # Untested
        #
        
        while self.in_progress:
            pass
    
    def start_new_round(self):
        """
        Initiates a new round of Blackjack.

        - 1. Betting Phase:
            - 1.1 Dealer takes bets from players at the table.

        - 2. Initial Deal:
            - 2.1 Dealer deals two cards for every player who has placed a bet.
            - 2.2 Dealer deals two cards for themselves, one face-up and one face-down.

        - 3. Check for Naturals:
            - 3.1 If the dealer's face-up card is not an Ace or a 10-point card, skip this of this step.
            - 3.2 If player rejects insurance, skip the rest of this step.
            - 3.3 Collect half of the player's original bet for insurance.

        - 5. Player Actions:
            - 5.1 Progressing clockwise through players and within player's active hands:
                - 5.1.1 Split Pairs:
                        - 5.1.1.1 If the player's initial two cards are not of the same rank, skip the rest of step 5.1.1.
                        - 5.1.1.2 If player rejects split request, skip the rest of step 5.1.1.
                        - 5.1.1.3 Take second card from player hand and use as first card for new hand.
                        - 5.1.1.4 Deal one card to original hand and one card to newly created hand.
                - 5.1.2 Double Down:
                        - 5.1.2.1 Player can double their original bet and receive only one more card.
                - 5.1.3 Hit:
                        - 5.1.3.1 If player rejects hit request(i.e. player stands), player keeps their current hand total and moves to the next player/hand.
                        - 5.1.3.2 Dealer deals card to player hand.
                        - 5.1.3.3 Repeat until the player stands or busts (hand value over 21).

        6. Dealer's Turn:
            - 6.1 Once all players have completed their actions, the dealer reveals their face-down card.
            - 6.2 The dealer hits until they have a total of 17 or higher.
            - 6.3 If the dealer busts, all remaining players win.

        7. Compare Hands:
            7.1 Compare each player's hand to the dealer's hand:
                7.1.1 Win:
                        7.1.1.1 Players with a higher hand total than the dealer win.
                7.1.2 Push (Tie):
                        7.1.2.1 Players with the same hand total as the dealer receive their bet back.
                7.1.3 Lose:
                        7.1.3.1 Players with a lower hand total than the dealer lose their bet.

        8. Payouts:
            8.1 Pay winning players according to the game rules.

        9. Even Money Option:
            9.1 If a player has a blackjack and the dealer's face-up card is an Ace, offer even money.
                9.1.1 Player can choose to take even money (1:1 payout) or decline.

        10. Round End:
            10.1 Collect losing bets and pay winning bets.
        """
        
        # Initiate new round
        self.current_round = Round(dealer=self.dealer)
        print("Initiating new round")
        
        # STEP 1 - Betting phase
        self.current_round.send_bet_requests(all_players=self.all_players)      
        
        # STEP 2 - Initial deal
        # 2.1 Dealer deals two cards for every player who has placed a bet
        # 2.2 Dealer deals two cards for themselves, one face-up and one face-down.
        self.dealer.deal_initial_cards(table_deck=self.table_deck, participating_players=self.current_round.participating_players)
        
        # STEP 3 - Check for neutrals
        # 3.1 If the dealer's face-up card is an Ace or a 10-value card, offer players insurance.
        self.current_round.send_insurance_requests(dealer=self.dealer)
        
        # To be refactored for 4.1.1
        self.current_round.send_split_requests(dealer=self.dealer, table_deck=self.table_deck)
        
        # Step 4 - Player Actions
        #4.1 Progressing clockwise through players and within player's active hands
        for player in self.current_round.participating_players:
            # 4.1.1 Split
            for hand in player.hands:
                # 4.1.2 Double down
                if player.request_double_down(hand=hand):
                    self.dealer.double_down_player_hand(player_hand=hand, player=player, table_deck=self.table_deck)
                # 4.1.3 Hit
                while hand.is_busted() == False and player.request_double_down(hand=hand):
                    self.dealer.hit_player_hand(hand=hand, table_deck=self.table_deck)
                
                hand.deactivate()
        
        # Step 6 - Dealer's turn
        # 6.1 - Dealer reveals face-down card
        self.dealer.hand.cards[1].make_visible()
        # 6.2 - The dealer hits until they have a total of 17 or higher.
        while self.dealer.hand.is_busted() == False and self.dealer.hand.max_non_bust_score() < 18:
            self.dealer.deal_card(player_hand=self.dealer.hand, table_deck=self.table_deck)
            # Check for hand bust
            if self.dealer.hand.max_non_bust_score() == 0:
                self.dealer.hand.set_busted()
                    
    
    def add_player(self, player: Player):
        """
        Adds player to self.all_players list
        
        Player is not added if it is in list of all players
        """
        # Check if player is already in list
        if player in self.all_players:
            return
        self.all_players.append(player)
    
    def remove_player(self, player: Player):
        """
        Removes player from self.all_players list
        """
        # Check is player is in all_players list
        if player not in self.all_players:
            return
        self.all_players.remove(player)