import unittest
import copy
# Project files
from card import Card
from constants import Deck
from dealer import Dealer
from players.human import Human
from game import Game
from hand import Hand

# Sample objects
ace_of_spades = Card(rank="Ace", suit="Spades", points=1)
ace_of_hearts = Card(rank="Ace", suit="Hearts", points=1)
queen_of_diamonds = Card(rank="Queen", suit="Diamonds", points=10)
five_of_clubs = Card(rank="Five", suit="Clubs", points=5)
ten_of_hearts = Card(rank="Ten", suit="Hearts", points=10)


class test_dealer(unittest.TestCase):
    
    def test_deal_card_object_retention(self):
        """
        Validates retention of same object when card is transferred from table deck to player hand
        """
        table_deck = [ace_of_spades]
        player = Human(player_name="Test player")
        dealer = Dealer()
        
        dealer.deal_card(player_hand=player.hands[0], table_deck=table_deck)
        
        self.assertEquals(player.hands[0].cards[0], ace_of_spades)
        
    
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
        player = Human(player_name="test" , custom_starting_hands=[main_hand_before_split])
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

class test_hand(unittest.TestCase):
    
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
        
class test_card(unittest.TestCase):
    
    def test_full_names(self):
        self.assertEqual("Ace of Spades", ace_of_spades.full_name())

class test_deck_creation(unittest.TestCase):
    
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

class test_player(unittest.TestCase):
    pass

class test_round(unittest.TestCase):
    pass



if __name__ == '__main__':
    unittest.main()