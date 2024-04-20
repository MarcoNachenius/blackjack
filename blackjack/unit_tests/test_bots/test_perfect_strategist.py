import unittest
import numpy as np

from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
import blackjack.players.bots.perfect_strategist.strategy_matrixes as strategy_matrixes
from blackjack.strategy_manager.strategy_matrixes.soft_totals import SoftTotalStrategy
from blackjack.strategy_manager.strategy_matrixes.hard_totals import HardTotalStrategy
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
        # Test double down

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

class TestSoftTotalPermutations(unittest.TestCase):
    
    def test_next_permutations(self):
        test_player = PerfectStrategist(player_name="test_player")
        next_permutation = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #21
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #18
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #17
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #16
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #12
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #11
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10
            [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], #9
            [3, 3, 3, 3, 3, 0, 0, 1, 1, 1], #8
            [1, 2, 2, 2, 2, 1, 1, 1, 1, 1], #7
            [1, 1, 2, 2, 2, 1, 1, 1, 1, 1], #6
            [1, 1, 2, 2, 2, 1, 1, 1, 1, 1], #5
            [1, 1, 1, 2, 2, 1, 1, 1, 1, 1], #4
            [1, 1, 1, 2, 2, 1, 1, 1, 1, 1], #3
            [1, 1, 1, 2, 2, 1, 1, 1, 1, 2]  #2
        ], dtype= int)
        
        # Get new permutation based on current soft total strategy matrix
        generated_value = test_player.soft_total_strategy.generate_next_permutation(current_matrix=test_player.soft_total_strategy.get_strategy_matrix())
        self.assertEqual(generated_value.all(), next_permutation.all())
        
        # Test complete transition
        pre_transition_matrix = np.array([
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #21
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #20
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #19
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #18
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #17
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #16
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #15
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #14
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #13
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #12
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #11
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #10
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #9
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #8
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #7
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #6
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #5
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #4
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #3
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]  #2
        ], dtype= int)
        
        post_transition_matrix = SoftTotalStrategy.generate_next_permutation(pre_transition_matrix)
        self.assertEqual(post_transition_matrix.all(), np.zeros(shape=(20,10), dtype=int).all())

class TestHardTotalPermutations(unittest.TestCase):
    
    def test_next_permutations(self):
        test_player = PerfectStrategist(player_name="test_player")
        next_permutation = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #21
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #18
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #17
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #16
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #15
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #14
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #13
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1], #12
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], #11
            [2, 2, 2, 2, 2, 2, 2, 2, 0, 0], #10
            [0, 2, 2, 2, 2, 0, 0, 0, 0, 0], #9
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #8
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #7
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #6
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #5
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]  #4
        ], dtype= int)
        
        # Get new permutation based on current soft total strategy matrix
        generated_value = test_player.hard_total_strategy.generate_next_permutation(current_matrix=test_player.soft_total_strategy.get_strategy_matrix())
        self.assertEqual(generated_value.all(), next_permutation.all())
        
        # Test complete transition
        pre_transition_matrix = np.array([
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #21
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #20
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #19
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #18
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #17
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #16
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #15
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #14
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #13
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #12
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #11
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #10
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #9
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #8
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #7
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #6
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7], #5
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]  #4
        ], dtype= int)
        
        post_transition_matrix = HardTotalStrategy.generate_next_permutation(pre_transition_matrix)
        self.assertEqual(post_transition_matrix.all(), np.zeros(shape=(18,10), dtype=int).all())