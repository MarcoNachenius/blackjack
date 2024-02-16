import copy
# Project files
from card import Card
from constants import Deck
from dealer import Dealer
from game import Game
from hand import Hand
from round import Round
# Player objects
from players.human import Human
from players.bots.yesman import Yesman
from players.bots.noman import Noman

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
# Test hands
table_deck = [queen_of_diamonds, ten_of_hearts, seven_of_clubs, eight_of_diamonds, two_of_hearts, three_of_spades, four_of_clubs]
hand_with_two_fives = Hand(starting_hand=[five_of_clubs, five_of_clubs])
hand_with_two_aces = Hand(starting_hand=[five_of_clubs, five_of_clubs])
non_pair_hand = Hand(starting_hand=[seven_of_clubs, eight_of_diamonds])
# Test hand groups
two_hands_with_two_pairs = [hand_with_two_fives, hand_with_two_fives]
three_hands_with_two_pairs = [hand_with_two_aces, non_pair_hand, hand_with_two_fives] # Non-pair in middle of list
four_hands_with_one_pair = [non_pair_hand, non_pair_hand, hand_with_two_aces, non_pair_hand]
# Test players
dealer = Dealer()
yesman_without_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=[non_pair_hand])
yesman_with_two_hands_with_two_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
yesman_with_enough_for_one_split = Yesman(player_name="", custom_starting_chips=10, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))        
broke_yesman_with_two_pairs = Yesman(player_name="", custom_starting_chips=1, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
yesman_with_three_hands_with_two_pairs = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(three_hands_with_two_pairs))
yesman_with_four_hands_with_one_pair = Yesman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(four_hands_with_one_pair))
noman_with_two_hands_with_two_pairs = Noman(player_name="", custom_starting_chips=100, custom_initial_bet_amount=10, custom_starting_hands=copy.deepcopy(two_hands_with_two_pairs))
# Player groups
unaffected_players = [broke_yesman_with_two_pairs, noman_with_two_hands_with_two_pairs, yesman_with_four_hands_with_one_pair, yesman_without_pairs]
single_split_players = [yesman_with_enough_for_one_split, yesman_with_three_hands_with_two_pairs]
multiple_split_players = [yesman_with_two_hands_with_two_pairs]

for hand in yesman_with_two_hands_with_two_pairs.hands:
    for card in hand.cards:
        print(card.rank)
    print("")
round = Round(participating_players=multiple_split_players)
round.send_split_requests(dealer=dealer, table_deck=copy.deepcopy(table_deck))
print("executed method\n")
for hand in yesman_with_two_hands_with_two_pairs.hands:
    for card in hand.cards:
        print(card.rank)
    print("")