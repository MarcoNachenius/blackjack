from blackjack.players.player import Player
from blackjack.game_objects.dealer import Dealer
from blackjack.game_objects.round import Round
from blackjack.game_objects.card import Card
from blackjack import constants
from blackjack.print_statements import RoundStatements

from typing import List

class Game(object):
    """
    When the game object is initiated
    
    Table deck is loaded to 
    """
    def __init__(self, all_players: List[Player] = None, starting_deck: List[Card] = None):
        self.game_id: int = 0
        self.dealer: Dealer = Dealer()
        self.all_players: List[Player] = all_players
        self.in_progress = True
        self.current_round: Round = Round()
        self.table_deck = starting_deck or constants.Deck.starting_deck()
    
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
        - 3. Check for dealer blackjack
            - 3.1 Evaluate face-up card:
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
        self.current_round = Round()
        print("NEW ROUND INITIATED")
        print("TAKING BETS FROM PLAYERS")
        # STEP 1 - Betting phase
        self.current_round.send_bet_requests(all_players=self.all_players, dealer=self.dealer)      
        # Terminal Output
        for player in self.current_round.get_participating_players():
            RoundStatements.successful_bet_placed(player=player)
        
        # Check for lack of participating players
        if len(self.current_round.get_participating_players()) == 0:
            print("UNUSUAL ROUND ENDING: ROUND ENDED DUE TO LACK OF PARTICIPATING PLAYERS")
            return
        
        print("DEALING INITIAL HANDS")
        # STEP 2 - Initial deal
        # 2.1 Dealer deals two cards for every player who has placed a bet
        # 2.2 Dealer deals two cards for themselves, one face-up and one face-down.
        self.dealer.deal_initial_cards(table_deck=self.table_deck, participating_players=self.current_round.participating_players)
        # Terminal output
        RoundStatements.initial_deal_report(dealer_hand=self.dealer.hand, participating_players=self.current_round.get_participating_players())
        
        print("CHECKING FOR DEALER NATURAL")
        # STEP 3 - Check for naturals
        # 3.1 If the dealer's face-up card is an Ace, offer players insurance.
        if self.dealer.hand.cards[0].rank == "Ace":
            print("DEALER HAS ACE, SENDING INSURANCE REQUESTS")
            self.current_round.send_insurance_requests(dealer=self.dealer)
        # 3.2 - Evaluate face down card
        if self.dealer.hand.has_natural_blackjack():
            print("DEALER NATURAL BLACKJACK FOUND")
            self.current_round.conclude_insurance_round(dealer=self.dealer)
            self.current_round.clear_round_values(dealer=self.dealer)
            return
        
        # Step 4 - Player Actions
        #4.1 Progressing clockwise through players and within player's active hands
        for player in self.current_round.participating_players:
            for hand in player.hands:
                # 4.1.1 Split
                self.current_round.send_split_request(dealer=self.dealer, table_deck=self.table_deck, player=player, hand=hand)
                # 4.1.2 Double down
                self.current_round.send_double_down_request(dealer=self.dealer, table_deck=self.table_deck, player=player, hand=hand)                
                # 4.1.3 Hit
                self.current_round.send_hit_request(dealer=self.dealer, table_deck=self.table_deck, player=player, hand=hand)
                
        # Step 6 - Dealer's turn
        # 6.1 - Dealer reveals face-down card
        self.dealer.hand.cards[1].make_visible()
        # 6.2 - The dealer hits until they have a total of 17 or higher.
        while self.dealer.needs_to_hit_again(participating_players=self.current_round.participating_players):
            self.dealer.deal_card(player_hand=self.dealer.get_hand(), table_deck=self.table_deck)
        
        
        print("AWARDING WINS")
        self.current_round.award_wins_comparatively(dealer=self.dealer)
        RoundStatements.round_completion_results(dealer_hand=self.dealer.get_hand(), participating_players=self.current_round.get_participating_players())
        
    
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
            print("No player removed: Player is not in self.participating_players")
            return
        self.all_players.remove(player)
    
    # Getters and setters
    # GAME_ID
    def get_game_id(self) -> int:
        return self.game_id
    def set_game_id(self, game_id: int):
        self.game_id = game_id
    # IN_PROGRESS    
    def get_in_progress(self) -> bool:
        return self.in_progress    
    def set_in_progress(self, in_progress: bool):
        self.in_progress = in_progress
    # ALL_PLAYERS
    def get_all_players(self) -> List[Player]:
        return self.all_players
    def set_all_players(self, all_players: List[Player]):
        if not isinstance(all_players, list) or not all(isinstance(player, Player) for player in all_players):
            raise ValueError("all_players must be a list of Player instances\n")
        self.all_players = all_players
    # CURRENT_ROUND
    def get_current_round(self) -> Round:
        return self.current_round
    def set_current_round(self, round: Round):
        self.current_round = round
    # DEALER
    def set_dealer(self, dealer: Dealer):
        self.dealer = dealer
    def get_dealer(self) -> Dealer:
        return self.dealer
    