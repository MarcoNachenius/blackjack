from player import Player
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
    
    def play_new_round(self):
        
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
            - 3.4 Pay 2:1 on the insurance bet if the dealer has a natural blackjack.

        - 4. Check for Player Blackjack:
            - 4.1 If any player has a natural blackjack, pay them 3:2 on their bet.
            - 4.2 Remove player from round's participating players list

        - 5. Player Actions:
            - 5.1 Progressing clockwise through players and within player's active hands:
                - 5.1.1 Split Pairs:
                        5.1.4.1 If the player's initial two cards are of the same rank, they can split them into two separate hands.
                                5.1.4.1.1 Follow the steps 5.1.1.1 to 3.1.1.1.2 for each split hand.
                - 5.1.2 Double Down:
                        5.1.2.1 Player can double their original bet and receive only one more card.
                - 5.1.2 Hit:
                        5.1.1.1 Player takes an additional card to increase their hand total.
                        5.1.1.2 Repeat until the player stands or busts (hand value over 21).
                - 5.1.3 Stand:
                        5.1.2.1 Player keeps their current hand total and moves to the next player.
                

        6. Dealer's Turn:
            6.1 Once all players have completed their actions, the dealer reveals their face-down card.
            6.2 The dealer hits until they have a total of 17 or higher.
            6.3 If the dealer busts, all remaining players win.

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
        
        # STEP 1 - Betting phase 
        self.current_round.send_bet_requests(all_players=self.all_players)        
        
        # STEP 2 - Initial deal
        # 2.1 Dealer deals two cards for every player who has placed a bet
        self.dealer.deal_initial_cards(table_deck=self.table_deck, participating_players=self.current_round.participating_players)
        
        # STEP 3 - Check for neutrals
        # 3.1 If the dealer's face-up card is an Ace or a 10-value card, check for a natural blackjack
        self.current_round.send_insurance_requests()
        
        # STEP 4 - Check for Player Blackjack:
        #    4.1 If any player has a natural blackjack, pay them 3:2 on their bet.
        #    4.2 Skip to the end of the round for players with blackjack.
        self.current_round.award_natural_blackjack_wins(dealer=self.dealer, participating_players=self.current_round.participating_players)
        
        # Step 5 - Player Actions
        for player in self.current_round.participating_players:
            for hand in player.hands:
                
                # Step 5.1.1 - Split pairs
                while hand.is_splittable() and player.is_able_to_split():
                    # Send split request to player
                    if player.request_split_pair():
                        self.dealer.split_player_hand(split_hand=hand, player=player, table_deck=self.table_deck)
                
                # Step 5.1.2 - Double down 
                if player.is_able_to_double_down and player.request_double_down:
                    self.dealer.double_down_player_hand(hand=hand, player=player, table_deck=self.table_deck)
                
                # 
    
    def add_player(self, player: Player):
        """
        Adds player to self.all_players list
        """
        # Exceptions
        #
        # Untested
        #
        self.all_players.append(player)