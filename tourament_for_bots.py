"""
This program simulates a tournament-style between multiple players.

Winning player of a game will be declared when:
- Player has the most chips remaining after max limit of rounds
- Only one player still has enough chips to bet

"""
from blackjack.game_objects.game import Game
from blackjack.players.bots.perfect_strategist.perfect_strategist import PerfectStrategist
from blackjack.players.bots.bot_builder import BotBuilder
from blackjack.database_manager.db_builder import DatabaseBuilder
from blackjack.database_manager.db_setters import DatabaseSetters

amount_of_games = 5 # Amount of games that will be played where all players start with same balance
max_number_of_rounds = 1000
rounds_played = 0
winner = None

if __name__ == "__main__":
    #database = DatabaseBuilder()
    #database.create_database()
    #db_updater = DatabaseSetters()
    
    # Create game and player objects
    all_players = [PerfectStrategist("The GOAT"), BotBuilder.return_random_player(), BotBuilder.return_random_player(), PerfectStrategist("The GOAT"), PerfectStrategist("The other GOAT")]
    game = Game(all_players=all_players)
    # Create Players row
    #for player in game.get_all_players():
    #    database.insert_into_players(player_name=player.get_player_name(), balance=player.get_chips())
    #    player.set_player_id(database.get_last_id_players())
    ## Create Games row
    #database.insert_into_games()
    #game.set_game_id(database.get_last_id_games())

    while rounds_played != max_number_of_rounds:
        # Start new round
        game.start_new_round()
        # Create Rounds.DealerHandID db value
    #    database.insert_into_hand_history(hand_combo_id=0, is_doubled_down="False", outcome="DEALER HAND")
        # Set Dealer.hand_id
    #    game.get_dealer().set_hand_id(database.get_last_hand_id())
        # Create CardHistory rows for dealer hand
    #    for card in game.get_dealer().get_hand().get_cards():
    #        database.insert_into_card_history(hand_id=game.get_dealer().get_hand_id(), card_name=card.full_name())
        # Create Rounds row
    #    database.insert_into_rounds(game_id=game.get_game_id(), dealer_hand_id=game.get_dealer().get_hand_id())
        # Set Round.round_id
    #    game.get_current_round().set_round_id(database.get_last_id_rounds())
    #    for player in game.get_all_players():
    #        # Create PlayerHistory row
    #        database.insert_into_player_history(player_id=player.get_player_id(),
    #                                            round_id=game.get_current_round().get_round_id(),
    #                                            is_insured=str(player.get_is_insured()),
    #                                            initial_bet=player.get_initial_bet_amount())
    #        # Set Player.hand_combo_id
    #        player.set_hand_combo_id(database.get_last_hand_combo())
    #        for hand in player.get_hands():
    #            # Create HandHistory row
    #            database.insert_into_hand_history(hand_combo_id=player.get_hand_combo_id(), is_doubled_down=str(hand.is_doubled_down()), outcome=hand.get_final_outcome())
    #            # Set Hand.hand_id
    #            hand.set_hand_id(database.get_last_hand_id())
    #            for card in hand.get_cards():
    #                # Create CardHistory rows for player hand
    #                database.insert_into_card_history(hand_id=hand.get_hand_id(), card_name=card.full_name())

        
        rounds_played += 1
        if len(game.current_round.get_participating_players()) == 0:
            print(f'Both players lost')
            break
        # Check for winner
        if len(game.current_round.get_participating_players()) == 1:
            winner = game.current_round.get_participating_players()[0]
            print(f'{game.current_round.get_participating_players()[0].get_player_name()} has won the game')
            break
        game.current_round.clear_round_values(dealer=game.get_dealer())
        
    
    
    
    
    #database.connection.close()
    #db_updater.connection.close()
    print("\nGame successfully completed!")
    print(f'Rounds played: {rounds_played}')
    #database.delete_database()
    