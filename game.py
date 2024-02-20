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
        
        1. Betting Phase:

        1.1 Dealer takes bets from players at the table.
        
        2. Initial Deal:

        2.1 Dealer deals two cards for every player who has placed a bet.
        2.2 Dealer deals two cards for themselves, one face-up and one face-down.
        3. Insurance Offer and Dealer's Peek for Blackjack:

        3.1 If the dealer's face-up card is an Ace or a 10-point card, the dealer peeks at their face-down card for blackjack (without revealing it to players).
        3.1.1 Offer insurance to players if the dealer's face-up card is an Ace.
        3.1.1.1 If a player accepts insurance, collect half of the player's original bet for insurance.
        3.1.1.2 If a player rejects insurance, proceed to the next player.
        3.1.2 If the dealer has a blackjack, insurance bets are paid out 2:1. The round ends for players with no blackjack, except for players who also have a blackjack, resulting in a push.
        3.1.3 If the dealer does not have a blackjack, play continues to player actions.
        4. Player Actions:

        4.1 Allow each player to act on their hand, progressing clockwise:
        4.1.1 Split Pairs:
        4.1.1.1 Offer to split if the player's initial two cards are of the same rank.
        4.1.1.2 If player accepts split, proceed as described. If player rejects, move to the next action.
        4.1.2 Double Down:
        4.1.2.1 Offer double down. If accepted, player doubles their bet and receives only one more card.
        4.1.3 Hit/Stand:
        4.1.3.1 Players decide to hit or stand.
        4.1.3.2 Continue until the player stands or busts.
        5. Dealer's Turn:

        5.1 After all players have completed their actions, dealer reveals their face-down card.
        5.2 Dealer hits until their total is 17 or higher, including soft 17.
        6. Compare Hands:

        6.1 Compare each player's hand against the dealer's:
        6.1.1 Win: Players with a higher total than the dealer win.
        6.1.2 Push: Players with the same total as the dealer push.
        6.1.3 Lose: Players with a lower total than the dealer lose.
        7. Payouts:

        7.1 Pay winning players and collect losing bets.
        8. Round End:

        8.1 Clear the table of cards and prepare for the next round.
        
        
        Initiates a new round of Blackjack.

        - 1. Betting Phase:
            - 1.1 Dealer takes bets from players at the table.

        - 2. Initial Deal:
            - 2.1 Dealer deals two cards for every player who has placed a bet.
            - 2.2 Dealer deals two cards for themselves, one face-up and one face-down.
        - 3. Check for dealer blackjack
            - 3.1 Evaluate face up card:
                - 3.1.1 If the dealer's face-up card is not an Ace, skip the rest of step 3.
                - 3.1.2 If player rejects insurance, skip the rest of this step.
                - 3.1.3 Collect half of the player's original bet for insurance.
            - 3.2 Evaluate face-down card:
                - 3.2.1 If the dealer's face-down card is not a 10-point card, skip the rest of this step
                - 3.2.2 Pay 2:3 of the insurance bet to players who chose insurance
                - 3.2.3 Award loss to all players that do not have natural blackjack
                - 3.2.3 Award push to all players that have natural blackjack
                - 3.2.4 Skip all subsequent steps and start new round
        
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
        # 3.1 If the dealer's face-up card is an Ace, offer players insurance.
        if self.dealer.hand.cards[0].rank == "Ace":
            self.current_round.send_insurance_requests(dealer=self.dealer)
        # 3.2 - Evaluate face down card
        if self.dealer.hand.has_natural_blackjack():
            self.current_round.conclude_insurance_round(dealer=self.dealer)
            return
        
        # Step 4 - Player Actions
        #4.1 Progressing clockwise through players and within player's active hands
        for player in self.current_round.participating_players:
            for hand in player.hands:
                # 4.1.1 Split
                if hand.is_splittable() and player.is_able_to_split() and player.request_split_pair():
                    self.dealer.split_player_hand(split_hand=hand, player=player, table_deck=self.table_deck)
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
        while self.dealer.hand.max_non_bust_score() > 0 and self.dealer.hand.max_non_bust_score() < 18:
            self.dealer.deal_card(player_hand=self.dealer.hand, table_deck=self.table_deck)
        
        # Check for dealer hand bust
        if self.dealer.hand.max_non_bust_score() == 0:
            self.dealer.hand.set_bust(False)
            self.current_round.award_dealer_bust_wins(dealer=self.dealer)
            return
        
        self.dealer.award_wins_comparatively()
    
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