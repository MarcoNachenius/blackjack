import unittest
from card import Card
from players.bots.yesman import Yesman
from dealer import Dealer

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
class test_play_new_round(unittest.TestCase):
    
    def test_deal_next_card(self):
        """
        Tests the non-random dealing of cards where the first card of the
        table deck is drawn from an unshuffled deck.
        """
        dealer = Dealer()
        
    def test_potential_infinite_split(self):
        """
        Tests the splitting threshold of a player who
        always accepts split requests
        """