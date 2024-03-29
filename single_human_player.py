from blackjack.game import Game
from blackjack.players.human import Human
from blackjack.players.bots.yesman import Yesman
from blackjack.database_builder import DatabaseBuilder

import os

if __name__ == "__main__":
    db_name = 'blackjack.db'
    database = DatabaseBuilder(db_name=db_name)
    database.create_database()
    all_players = [Human(player_name="Foo")]
    game = Game(all_players=all_players)
    
    
    # Create Players row
    for player in game.get_all_players():
        database.insert_into_players(player_name=player.get_player_name(), balance=player.get_chips())
        player.set_player_id(database.get_last_id_players())
    # Create Games row
    database.insert_into_games()
    game.set_game_id(database.get_last_id_games())
    # Start new round
    game.start_new_round()
    # Create Rounds.DealerHandID db value
    database.insert_into_hand_history(hand_combo_id=0, is_doubled_down="False", outcome="DEALER HAND")
    # Set Dealer.hand_id
    game.get_dealer().set_hand_id(database.get_last_hand_id())
    # Create CardHistory rows for dealer hand
    for card in game.get_dealer().get_hand().get_cards():
        database.insert_into_card_history(hand_id=game.get_dealer().get_hand_id(), card_name=card.full_name())
    # Create Rounds row
    database.insert_into_rounds(game_id=game.get_game_id(), dealer_hand_id=game.get_dealer().get_hand_id())
    # Set Round.round_id
    game.get_current_round().set_round_id(database.get_last_id_rounds())
    for player in game.get_all_players():
        # Create PlayerHistory row
        database.insert_into_player_history(player_id=player.get_player_id(),
                                            round_id=game.get_current_round().get_round_id(),
                                            is_insured=str(player.get_is_insured()),
                                            initial_bet=player.get_initial_bet_amount())
        # Set Player.hand_combo_id
        player.set_hand_combo_id(database.get_last_hand_combo())
        for hand in player.get_hands():
            # Create HandHistory row
            database.insert_into_hand_history(hand_combo_id=player.get_hand_combo_id(), is_doubled_down=hand.is_doubled_down(), outcome=hand.get_final_outcome())
            # Set Hand.hand_id
            hand.set_hand_id(database.get_last_hand_id())
            for card in hand.get_cards():
                # Create CardHistory rows for player hand
                database.insert_into_card_history(hand_id=hand.get_hand_id(), card_name=card.full_name())
        
    game.current_round.clear_round_values(dealer=game.get_dealer())
    another_round_request = input("Play another round? [y/n]")
    while another_round_request == "y":
        game.start_new_round()
        another_round_request = input("Play another round? [y/n]")
    database.connection.close()
    os.remove(f'./{db_name}')
    