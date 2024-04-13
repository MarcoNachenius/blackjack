import unittest

from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
import blackjack.players.bots.perfect_strategist.strategy_matrixes as strategy_matrixes
from blackjack.game_objects.card import Card
from blackjack.game_objects.hand import Hand

# Sample Cards
ace_of_spades = Card(rank="Ace", suit="Spades", points=1)
two_of_hearts = Card(rank="Two", suit="Hearts", points=2)
three_of_spades = Card(rank="Three", suit="Spades", points=3)
four_of_clubs = Card(rank="Four", suit="Clubs", points=4)
five_of_clubs = Card(rank="Five", suit="Clubs", points=5)
six_of_diamonds = Card(rank="Six", suit="Diamonds", points=6)
seven_of_clubs = Card(rank="Seven", suit="Clubs", points=7)
eight_of_diamonds = Card(rank="Eight", suit="Diamonds", points=8)
nine_of_spades = Card(rank="Nine", suit="Spades", points=9)
ten_of_hearts = Card(rank="Ten", suit="Hearts", points=10)
jack_of_spades = Card(rank="Jack", suit="Spades", points=10)
queen_of_diamonds = Card(rank="Queen", suit="Diamonds", points=10)


class TestHardTotalStrategy(unittest.TestCase):
    
    def test_set_action_number(self):
        test_player = PerfectStrategist(player_name="test_player")
        # Test transfer of hard total matrix
        self.assertEqual(test_player.hard_total_strategy.get_strategy_matrix().all(), strategy_matrixes.hard_totals.all())
        # Test actions when player hard total is 9
        nine_point_hard_total = Hand(starting_hand=[two_of_hearts, seven_of_clubs])
        test_player.set_hands([nine_point_hard_total])
        player_score = test_player.get_hands()[0].highest_score()
        # Test when dealer upcard is Two
        dealer_upcard_score = two_of_hearts.points
        action_number = test_player.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score)
        self.assertEqual(action_number, 0)
        # Change action number
        test_player.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score, new_action_number=3)
        # Retrieve action number
        action_number = test_player.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score)
        # Execute test
        self.assertEqual(action_number, 3)
        
    
    def test_double_down_action_numbers(self):
        
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test actions when player hard total is 9
        nine_point_hard_total = Hand(starting_hand=[two_of_hearts, seven_of_clubs])
        test_player.set_hands([nine_point_hard_total])
        player_score = test_player.get_hands()[0].highest_score()
        # Test when dealer upcard is Two
        dealer_upcard_score = two_of_hearts.points
        action_number = test_player.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score)
        self.assertEqual(action_number, 0)
        # Test when dealer upcard is Three
        dealer_upcard_score = three_of_spades.points
        action_number = test_player.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score)
        self.assertEqual(action_number, 2)
        # Test when dealer upcard is Ten
        dealer_upcard_score = ten_of_hearts.points
        action_number = test_player.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_hard_total=player_score)
        self.assertEqual(action_number, 0)
    
    def test_double_down_acceptance(self):
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test actions when player hard total is 9
        nine_point_hard_total = Hand(starting_hand=[two_of_hearts, seven_of_clubs])
        test_player.set_hands([nine_point_hard_total])
        
        # Test when dealer upcard is Two
        dealer_upcard = two_of_hearts
        action = test_player.request_double_down(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertFalse(action)
        
        # Test when dealer upcard is Three
        dealer_upcard = three_of_spades
        action = test_player.request_double_down(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertTrue(action)

class TestSoftTotalStrategy(unittest.TestCase):
    
    def test_get_and_set_action_number(self):
        
        test_player = PerfectStrategist(player_name="test_player")
        # Test transfer of soft total matrix
        self.assertEqual(test_player.soft_total_strategy.get_strategy_matrix().all(), strategy_matrixes.soft_totals.all())
        # Test actions when player soft total is 8
        eight_point_soft_total = Hand(starting_hand=[ace_of_spades, seven_of_clubs])
        test_player.set_hands([eight_point_soft_total])
        player_score = test_player.get_hands()[0].lowest_score()
        # Test when dealer upcard is Two
        dealer_upcard_score = two_of_hearts.points
        action_number = test_player.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_soft_total=player_score)
        self.assertEqual(action_number, 3)
        # Test when dealer upcard is Seven
        dealer_upcard_score = seven_of_clubs.points
        action_number = test_player.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_soft_total=player_score)
        self.assertEqual(action_number, 0)
        # Test when dealer upcard is Nine
        dealer_upcard_score = nine_of_spades.points
        action_number = test_player.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_soft_total=player_score)
        self.assertEqual(action_number, 1)
        # Test change in action number to 3
        action_number = 3
        test_player.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard_score, player_soft_total=player_score, new_action_number= action_number)
        self.assertEqual(test_player.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard_score, player_soft_total=player_score), 3)
        
    def test_double_down_acceptance(self):
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test actions when player soft total is 9
        nine_point_soft_total = Hand(starting_hand=[eight_of_diamonds, ace_of_spades])
        test_player.set_hands([nine_point_soft_total])
        
        # Test when dealer upcard is Two
        dealer_upcard = two_of_hearts
        action = test_player.request_double_down(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertFalse(action)
        
        # Test when dealer upcard is Six
        dealer_upcard = six_of_diamonds
        action = test_player.request_double_down(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertTrue(action)

class TestSplitPairStrategy(unittest.TestCase):
    
    def test_get_and_set_action_number(self):
        
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test transfer of split pair matrix
        self.assertEqual(test_player.split_pair_strategy.get_strategy_matrix().all(), strategy_matrixes.split_pairs.all())
        
        # Test actions when player has pair of nines
        nine_pair_hand = Hand(starting_hand=[nine_of_spades, nine_of_spades])
        test_player.set_hands([nine_pair_hand])
        
        # Test when dealer upcard is Four
        upcard_score = four_of_clubs.points
        player_score = test_player.get_hands()[0].lowest_score()
        action_number = test_player.split_pair_strategy.get_action_number(dealer_upcard_points=upcard_score, split_pair_score=player_score)
        self.assertEqual(action_number, 1)
        
        # Test when dealer upcard is Seven
        upcard_score = seven_of_clubs.points
        player_score = test_player.get_hands()[0].lowest_score()
        action_number = test_player.split_pair_strategy.get_action_number(dealer_upcard_points=upcard_score, split_pair_score=player_score)
        self.assertEqual(action_number, 0)
    
    def test_split_pair_acceptance(self):
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test action number when player has pair of Nines
        nine_pair = Hand(starting_hand=[nine_of_spades, nine_of_spades])
        test_player.set_hands([nine_pair])
        
        # Test when dealer upcard is Two
        dealer_upcard = two_of_hearts
        action = test_player.request_split_pair(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertTrue(action)
        
        # Test when dealer upcard is Seven
        dealer_upcard = seven_of_clubs
        action = test_player.request_split_pair(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertFalse(action)

class TestHitStrategy(unittest.TestCase):
    
    def test_hit_acceptance_with_soft_total(self):
        test_player = PerfectStrategist(player_name="test_player")
        
        # Test actions when player soft total is 8
        nine_point_soft_total = Hand(starting_hand=[seven_of_clubs, ace_of_spades])
        test_player.set_hands([nine_point_soft_total])
        
        # Test when dealer upcard is Two
        dealer_upcard = two_of_hearts
        action = test_player.request_hit(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertFalse(action)
        
        # Test when dealer upcard is Nine
        dealer_upcard = nine_of_spades
        action = test_player.request_hit(dealer_upcard=dealer_upcard, hand=test_player.get_hands()[0])
        self.assertTrue(action)