import unittest
import copy
# Project files
from blackjack.game_objects.card import Card
from blackjack.constants import Deck
from blackjack.game_objects.dealer import Dealer
from blackjack.game_objects.game import Game
from blackjack.game_objects.hand import Hand
from blackjack.game_objects.round import Round
# Player objects
from blackjack.players.human import Human
from blackjack.players.bots.yesman import Yesman
from blackjack.players.bots.noman import Noman

# Sample Cards
ace_of_spades = Card(rank="Ace", suit="Spades", points=1)
ace_of_hearts = Card(rank="Ace", suit="Hearts", points=1)
two_of_hearts = Card(rank="Two", suit="Hearts", points=2)
three_of_spades = Card(rank="Three", suit="Spades", points=3)
four_of_clubs = Card(rank="Four", suit="Clubs", points=4)
five_of_clubs = Card(rank="Five", suit="Clubs", points=5)
seven_of_clubs = Card(rank="Seven", suit="Clubs", points=7)
eight_of_diamonds = Card(rank="Eight", suit="Diamonds", points=8)
ten_of_hearts = Card(rank="Ten", suit="Hearts", points=10)
queen_of_diamonds = Card(rank="Queen", suit="Diamonds", points=10)


class TestDealer(unittest.TestCase):
    
    def test_deal_card_object_retention(self):
        """
        Validates retention of same object when card is transferred from table deck to player hand
        """
        table_deck = [ace_of_spades]
        player = Human(player_name="Test player")
        dealer = Dealer()
        
        dealer.deal_card(player_hand=player.hands[0], table_deck=table_deck)
        
        self.assertEqual(player.hands[0].cards[0], ace_of_spades)
        
    def test_deal_card_in_game(self):
        """
        Verify transfer of card from deck and into player hand
        
        Possible defect:
        - Verify dealer card no longer in 
        """
        # Verify transfer of card from deck
        deck_of_four_cards = [ace_of_spades, ace_of_hearts, queen_of_diamonds, five_of_clubs]
        player = Human(player_name="Test player")
        game = Game(starting_deck=deck_of_four_cards)
        
        card_successfully_transferred = True
        
        # Save the initial state for comparison
        initial_dealer_deck = list(game.table_deck)
        initial_player_hand = copy.deepcopy(player.hands[0])
        # Deal a card
        game.dealer.deal_card(player_hand=player.hands[0], table_deck=deck_of_four_cards)
        # Verify that the card has been removed from dealer's deck
        self.assertNotEqual(initial_dealer_deck, game.table_deck)
        self.assertEqual(len(initial_dealer_deck) - 1, len(game.table_deck))
        # Verify that the card has been added to the player's hand
        self.assertNotEqual(initial_player_hand, player.hands[0])
        self.assertEqual(len(initial_player_hand.cards) + 1, len(player.hands[0].cards))
        # Verify that player card is the one that is no longer in table deck
        for card in game.table_deck:
            for player_hand in player.hands:
                for player_card in player_hand.cards:
                    if card.full_name == player_card.full_name:
                        card_successfully_transferred = False
                        break
        self.assertTrue(card_successfully_transferred)
    
    def test_deal_initial_cards(self):
        test_player = Human(player_name="Test Player")
        dealer = Dealer()
        table_deck = [ace_of_spades, ten_of_hearts, queen_of_diamonds, five_of_clubs]
        
        # Verify values before method execution
        self.assertEqual(len(table_deck), 4)
        self.assertEqual(len(test_player.hands[0].cards), 0)
        self.assertEqual(len(dealer.hand.cards), 0)
        
        # Execute method
        dealer.deal_initial_cards(table_deck=table_deck, participating_players=[test_player])
        
        # Verify values after method execution
        self.assertEqual(len(table_deck), 0)
        self.assertEqual(len(test_player.hands[0].cards), 2)
        self.assertEqual(len(dealer.hand.cards), 2)
        
    def test_split_player_hand(self):
        main_hand_card = ace_of_spades
        split_hand_card = ace_of_hearts
        table_deck = [queen_of_diamonds, five_of_clubs]
        
        # Initial states
        main_hand_before_split = Hand(starting_hand=[main_hand_card, split_hand_card])
        # Altered states
        main_hand_after_split = Hand(first_card=main_hand_card)
        split_hand_after_split = Hand(first_card=split_hand_card)
        
        # Execute test
        player = Human(player_name="test" , custom_starting_hands=[main_hand_before_split], custom_starting_chips=500, custom_initial_bet_amount=10)
        dealer = Dealer()  
        dealer.split_player_hand(split_hand=main_hand_before_split, player=player, table_deck=table_deck)
        
        # Evaluate results
        self.assertEqual(player.hands[0].cards[0], main_hand_after_split.cards[0])
        self.assertTrue(player.hands[0].cards[1] == queen_of_diamonds or five_of_clubs)
        self.assertEqual(player.hands[1].cards[0], split_hand_after_split.cards[0])
        self.assertTrue(player.hands[1].cards[1] == queen_of_diamonds or five_of_clubs)
        # Check if cards have been removed from table deck
        self.assertTrue(len(table_deck) == 0)
        
    def test_insure_player(self):
        pass
    
    def test_double_down_hand(arg):
        pass

class TestHand(unittest.TestCase):
    
    def test_natural_blackjack(self):
        hand_with_natural_blackjack = Hand(starting_hand=[ace_of_hearts, ten_of_hearts])
        hand_without_natural_blackjack = Hand(starting_hand=[ace_of_hearts, five_of_clubs])
        self.assertTrue(hand_with_natural_blackjack.has_natural_blackjack())
        self.assertFalse(hand_without_natural_blackjack.has_natural_blackjack())
        
    def test_score_limits(self):
        hand_with_five_aces_and_ten =  Hand(starting_hand=[ace_of_hearts, ace_of_hearts, ace_of_hearts, ace_of_hearts, ace_of_hearts, ten_of_hearts])
        # Test lowest_score
        self.assertEqual(hand_with_five_aces_and_ten.lowest_score(), 15)
        # Test highest_score
        self.assertEqual(hand_with_five_aces_and_ten.highest_score(), 65)
    
    def test_max_non_bust_score(self):
        hand_with_five_aces_and_ten =  Hand(starting_hand=[ace_of_hearts, ace_of_hearts, ace_of_hearts, ace_of_hearts, ace_of_hearts, ten_of_hearts])
        self.assertEqual(hand_with_five_aces_and_ten.max_non_bust_score(), 15)
        hand_with_two_aces_and_five = Hand(starting_hand=[ace_of_hearts, ace_of_spades, five_of_clubs])
        self.assertEqual(hand_with_two_aces_and_five.max_non_bust_score(), 17)
        
    def test_full_names_list(self):
        hand = Hand(starting_hand=[ace_of_spades, queen_of_diamonds])
        self.assertEqual(hand.full_names_list(), ["Ace of Spades", "Queen of Diamonds"])
        
class TestCard(unittest.TestCase):
    
    def test_full_names(self):
        self.assertEqual("Ace of Spades", ace_of_spades.full_name())

class TestDeckCreation(unittest.TestCase):
    
    def test_point_values(self):
        full_deck = Deck.full_deck()
        ace_of_hearts_matched = False
        ace_of_spades_matched = False
        queen_of_diamonds_matched = False
        five_of_clubs_matched = False
        
        for card in full_deck:
            if not ace_of_hearts_matched:
                if card.full_name() == ace_of_hearts.full_name() and card.points == ace_of_hearts.points:
                    ace_of_hearts_matched = True
            if not ace_of_spades_matched:
                if card.full_name() == ace_of_spades.full_name() and card.points == ace_of_spades.points:
                    ace_of_spades_matched = True
            if not queen_of_diamonds_matched:
                if card.full_name() == queen_of_diamonds.full_name() and card.points == queen_of_diamonds.points:
                    queen_of_diamonds_matched = True
            if not five_of_clubs_matched:
                if card.full_name() == five_of_clubs.full_name() and card.points == five_of_clubs.points:
                    five_of_clubs_matched = True
        
        self.assertTrue(ace_of_hearts_matched)
        self.assertTrue(ace_of_spades_matched)
        self.assertTrue(queen_of_diamonds_matched)
        self.assertTrue(five_of_clubs_matched)

class TestGame(unittest.TestCase):
    
    def test_table_deck_capacity_deck(self):
        
        game = Game()
        # Reduce table deck capacity to an mount below allowed percentage
        game.table_deck = Deck.full_deck()
        # Perform initial state check
        self.assertEqual(len(game.table_deck), 52) # Should equal amount of two full decks
        # Perform test
        game.perform_table_deck_capacity_check()
        # Check that deck of cards has been successfully added to table deck
        self.assertEqual(len(game.table_deck), 104) # Should equal amount of two full decks

class TestRound(unittest.TestCase):
    
    def test_send_bet_request(self):
        pass

    def test_send_split_requests(self):
        # Test hands
        table_deck = [queen_of_diamonds, ten_of_hearts, seven_of_clubs, eight_of_diamonds, two_of_hearts, three_of_spades, four_of_clubs]
        hand_with_two_fives = Hand(starting_hand=[five_of_clubs, five_of_clubs])
        hand_with_two_aces = Hand(starting_hand=[five_of_clubs, five_of_clubs])
        non_pair_hand = Hand(starting_hand=[seven_of_clubs, eight_of_diamonds])
        # Test hand groups
        two_hands_with_two_pairs = [copy.deepcopy(hand_with_two_fives), copy.deepcopy(hand_with_two_fives)]
        three_hands_with_two_pairs = [hand_with_two_aces, non_pair_hand, hand_with_two_fives] # Non-pair in middle of list
        four_hands_with_one_pair = [non_pair_hand, non_pair_hand, hand_with_two_aces, non_pair_hand]
        # Test players
        dealer = Dealer()
        yesman_without_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=[non_pair_hand])
        yesman_with_two_hands_with_two_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
        yesman_with_enough_for_one_split = Yesman(player_name="", custom_starting_chips=10, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))        
        broke_yesman_with_two_pairs = Yesman(player_name="", custom_starting_chips=9, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
        yesman_with_three_hands_with_two_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(three_hands_with_two_pairs))
        yesman_with_four_hands_with_one_pair = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(four_hands_with_one_pair))
        noman_with_two_hands_with_two_pairs = Noman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
        # Player groups
        unaffected_players = [broke_yesman_with_two_pairs, noman_with_two_hands_with_two_pairs, yesman_with_four_hands_with_one_pair, yesman_without_pairs]
        single_split_players = [yesman_with_enough_for_one_split, yesman_with_three_hands_with_two_pairs]
        multiple_split_players = [yesman_with_two_hands_with_two_pairs]
        
        # UNAFFECTED PLAYERS
        # Initiate game
        game = Game(all_players=unaffected_players)
        # Verify initial states
        self.assertEqual(len(broke_yesman_with_two_pairs.hands), 2)
        self.assertEqual(len(noman_with_two_hands_with_two_pairs.hands), 2)
        self.assertEqual(len(yesman_with_four_hands_with_one_pair.hands), 4)
        self.assertEqual(len(yesman_without_pairs.hands), 1)
        # Execute Test
        unaffected_table_deck = copy.deepcopy(table_deck)
        # BROKE YESMAN WITH TWO PAIRS
        # Simulate execution of sending split requests 
        for hand in broke_yesman_with_two_pairs.get_hands():
            game.current_round.send_split_request(dealer=game.get_dealer(), table_deck=unaffected_table_deck, player=broke_yesman_with_two_pairs, hand=hand)
        self.assertEqual(len(broke_yesman_with_two_pairs.hands), 2)
        
        # Verify noman_with_two_hands_with_two_pairs
        self.assertEqual(len(noman_with_two_hands_with_two_pairs.hands), 2)
        # Verify yesman_with_four_hands_with_one_pair
        self.assertEqual(len(yesman_with_four_hands_with_one_pair.hands), 4)
        # Verify yesman_without_pairs
        self.assertEqual(len(yesman_without_pairs.hands), 1)
        
        ## Execute test
        #round.send_split_requests(dealer=dealer, table_deck=copy.deepcopy(table_deck))
        #
        ## Test single split players
        #round = Round(participating_players=single_split_players)
        #self.assertEqual(len(yesman_with_enough_for_one_split.hands), 2)
        ## Execute test
        #round.send_split_requests(dealer=dealer, table_deck=copy.deepcopy(table_deck))
        ## Verify yesman_with_enough_for_one_split
        #self.assertEqual(len(yesman_with_enough_for_one_split.hands), 3)
        ## Verify yesman_with_three_hands_with_two_pairs
        #self.assertEqual(len(yesman_with_three_hands_with_two_pairs.hands), 4)
        #
        ## Test multiple split players
        #round = Round(participating_players=multiple_split_players)
        #round.send_split_requests(dealer=dealer, table_deck=copy.deepcopy(table_deck))
        ## Verify yesman_with_two_hands_with_two_pairs
        #self.assertEqual(len(yesman_with_two_hands_with_two_pairs.hands), 4)
        
    def test_send_double_down_requests(self):
        pass
    
    #def test_send_insurance_requests(self):
    #    # Test objects
    #    yesman_with_enough_to_insure = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount= 50)
    #    yesman_without_enough_to_insure = Yesman(player_name="", custom_starting_chips=24, custom_initial_bet_amount= 50)
    #    noman = Yesman(player_name="Test Noman", custom_starting_chips=20, custom_initial_bet_amount= 50)
    #    participating_players = [yesman_with_enough_to_insure, noman]
    #    round = Round(participating_players=participating_players)
    #    dealer_with_potential_blackjack = Dealer(starting_hand=[ace_of_spades])
    #    dealer_without_potential_blackjack = Dealer(starting_hand=[five_of_clubs])
    #    # Initiate test where insurance requests should be sent
    #    round.send_insurance_requests(dealer=dealer_with_potential_blackjack)
    #    # Evaluate results
    #    self.assertEqual(yesman_with_enough_to_insure.chips, 75)
    #    self.assertEqual(yesman_without_enough_to_insure.chips, 24)
    #    self.assertEqual(noman.chips, 20)
    #    
    #    # Initiate test where insurance tests shouldn't be sent
    #    round.send_insurance_requests(dealer=dealer_without_potential_blackjack)
    #    # Evaluate results
    #    self.assertEqual(yesman_with_enough_to_insure.chips, 75)
    #    self.assertEqual(yesman_without_enough_to_insure.chips, 24)
    #    self.assertEqual(noman.chips, 20)


if __name__ == '__main__':
    unittest.main()