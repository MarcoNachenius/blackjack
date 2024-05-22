from typing import List

from blackjack.game_objects.card import Card
from blackjack.players.bots.strategist_abc import Strategist
from blackjack.game_objects.hand import Hand
from blackjack.strategy_manager.learning_bot_matrixes.learning_bot_strategies import LbStrategy
from blackjack.players.bots.learning_bot.round_moves_logger import LbRoundLog


class LearningBot(Strategist):
    '''
    LearningBot is a Player object that adjusts its strategy whenever a more preferential action presents itself.
    
    ### Strategy Matrixes
    LearningBot has hard total, soft total and split pair strategies that are derived from a Strategist bot's strategy matrixes.
    Strategy matrixes of LearningBot have the same height and width but are one dimension deeper. An action number in a strategy
    matrix refers to a list that is two values long on the corresponding memory matrix.
    
    ### Databases
    LearningBot is reliant on a 'memory' database that logs every move that has been made and its outcome.
    '''
    
    def __init__(self, player_name: str, custom_starting_hands: List[Hand] = None, custom_starting_chips: int = None, custom_initial_bet_amount: int = None):
        super().__init__(player_name=player_name ,custom_starting_hands=custom_starting_hands , custom_starting_chips=custom_starting_chips, custom_initial_bet_amount=custom_initial_bet_amount)
        self.lb_hard_total_memory_matrix = LbStrategy(height = 18, depth = 8)
        self.lb_soft_total_memory_matrix = LbStrategy(height = 20, depth = 8)
        self.lb_split_pair_memory_matrix = LbStrategy(height = 10, depth = 2)
        self.lb_hard_total_round_logs : List[LbRoundLog] = []
        self.lb_soft_total_round_logs : List[LbRoundLog] = []
        self.lb_split_pair_round_logs : List[LbRoundLog] = []
    
    def request_split_pair(self, dealer_upcard: Card, hand: Hand) -> bool:
        action_number = self.split_pair_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, split_pair_score=hand.lowest_score())
        round_strategy_logs = self.lb_split_pair_round_logs
        # Create log object
        action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number=action_number)
        # Add log to list if it is not already inside of it
        if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
            round_strategy_logs.append(action_log)
        accept_request = False
        action_number = self.split_pair_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, split_pair_score=hand.lowest_score())
        if action_number == 1:
            accept_request = True
        return accept_request
    
    def request_bet_amount(self) -> int:
        return 10
    
    def request_hit(self, dealer_upcard: Card, hand: Hand) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
            round_strategy_logs = self.lb_hard_total_round_logs
        else: # Assumes player's hand contains an Ace
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
            round_strategy_logs = self.lb_soft_total_round_logs
        
        # Create log object if dealer has ace (where all action numbers are applicable),
        # or if action number does not contain insurance decisions
        if dealer_upcard.points == 1  or action_number < 4:
            action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number=action_number)
            # Add log to list if it is not already inside of it
            if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                round_strategy_logs.append(action_log)
        
        # Check for hit
        if action_number == 1:
            return True
        # Check for double down, hit
        if action_number == 2:
            return True
        # Check for insurance, hit
        if action_number == 4:
            # Treat like action number 1(hit) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 1)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return True
        # Check for insurance, stand
        if action_number == 5:
            # Treat like action number 0(stand) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 0)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return False
        # Check for insurance, double down, hit
        if action_number == 6:
            # Treat like action number 2(double down, hit) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 2)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return True
        # Check for insurance, double down, stand
        if action_number == 7:
            # Treat like action number 3(double down, stand) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 3)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return False
        return False
    
    def request_double_down(self, dealer_upcard: Card, hand: Hand) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
            round_strategy_logs = self.lb_hard_total_round_logs
        else: # Assumes player's hand contains an Ace
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
            round_strategy_logs = self.lb_soft_total_round_logs
        
        # Create log object if dealer has ace (where all action numbers are applicable),
        # or if action number does not contain insurance decisions
        if dealer_upcard.points == 1  or action_number < 4:
            action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number=action_number)
            # Add log to list if it is not already inside of it
            if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                round_strategy_logs.append(action_log)
        
        # Check double down, hit
        if action_number == 2:
            return True
        # Check double down, stand
        if action_number == 3:
            return True
        # Check for insurance, hit
        if action_number == 4:
            # Treat like action number 1(hit) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 1)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return False
        # Check for insurance, stand
        if action_number == 5:
            # Treat like action number 0(stand) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 0)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return False
        # Check for insurance, double down, hit
        if action_number == 6:
            # Treat like action number 2(double down, hit) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 2)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return True
        # Check for insurance, double down, stand
        if action_number == 7:
            # Treat like action number 3(double down, stand) if dealer upcard is not Ace
            if dealer_upcard.points != 1:
                # Create incremented action_number
                new_action_number = (action_number + 1) % 8
                # Increment action number
                if hand.amount_of_aces() == 0:
                    self.hard_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total= hand.lowest_score(), new_action_number=new_action_number)
                else:
                    self.soft_total_strategy.set_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total= hand.lowest_score(), new_action_number=new_action_number)
                # Create log with adjusted action number
                action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number= 3)
                # Add log to list if it is not already inside of it
                if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
                    round_strategy_logs.append(action_log)
            return True
        return False
    
    def request_insurance(self, hand: Hand, dealer_upcard: Card) -> bool:
        """
        Action numbers:
        0 = Stand
        1 = Hit
        2 = Double down, hit 
        3 = Double down, stand
        4 = Insurance, hit
        5 = Insurance, stand
        6 = Insurance, double down, hit
        7 = Insurance, double down, stand
        """
        # Check for hard total value
        if hand.amount_of_aces() == 0:
            action_number = self.hard_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_hard_total=hand.lowest_score())
            round_strategy_logs = self.lb_hard_total_round_logs
        # Assumes player has hand containing at least one ace
        else: 
            action_number = self.soft_total_strategy.get_action_number(dealer_upcard_points=dealer_upcard.points, player_soft_total=hand.lowest_score())
            round_strategy_logs = self.lb_soft_total_round_logs
        
        # Create log object
        action_log = LbRoundLog(player_score=hand.lowest_score(), dealer_upcard_points=dealer_upcard.points, action_number=action_number)
        
        # Add log to list if it is not already inside of it
        if not self.contains_round_log(round_strategy_logs=round_strategy_logs, log_to_be_checked=action_log):
            round_strategy_logs.append(action_log)
        
        # Check insurance, hit
        if action_number == 4:
            return True
        # Check insurance, stand
        if action_number == 5:
            return True
        # Check for insurance, double down, hit
        if action_number == 6:
            return True
        # Check for insurance, double down, stand
        if action_number == 7:
            return True
        # Assumes action number instructs player to stand
        return False
    
    def clear_round_logs(self):
        """
        Clears hard total, soft total and split pair log lists
        """
        self.lb_hard_total_round_logs.clear()
        self.lb_soft_total_round_logs.clear()
        self.lb_split_pair_round_logs.clear()
    
    def log_hard_total_strategy_action(self, player_score : int, dealer_upcard_points: int, action_number: int):
        """
        Adds a LbRoundLog object to self.lb_hard_total_round_logs list.
        """
        # Create log object of hard total action
        move_log = LbRoundLog(player_score=player_score, dealer_upcard_points=dealer_upcard_points, action_number=action_number)
        # Add log to hard_totals 
        self.lb_hard_total_round_logs.append(move_log)
    
    def log_soft_total_strategy_action(self, player_score : int, dealer_upcard_points: int, action_number: int):
        """
        Adds a LbRoundLog object to self.lb_soft_total_round_logs list.
        """
        # Create log object of soft total action
        move_log = LbRoundLog(player_score=player_score, dealer_upcard_points=dealer_upcard_points, action_number=action_number)
        # Add log to soft_totals 
        self.lb_soft_total_round_logs.append(move_log)
    
    def log_split_pair_strategy_action(self, player_score : int, dealer_upcard_points: int, action_number: int):
        """
        Adds a LbRoundLog object to self.lb_split_pair_round_logs list.
        """
        # Create log object of split pair action
        move_log = LbRoundLog(player_score=player_score, dealer_upcard_points=dealer_upcard_points, action_number=action_number)
        # Add log to split_pairs 
        self.lb_split_pair_round_logs.append(move_log)
        
    def contains_round_log(self, round_strategy_logs: List[LbRoundLog], log_to_be_checked: LbRoundLog) -> bool:
        """
        Returns True if a log with the same values exists within a list of round logs.
        """
        found_identical_log = False
        for log in round_strategy_logs:
            # Check for identical player score
            if log.get_player_score() != log_to_be_checked.get_player_score():
                continue
            # Check for identical dealer upcard points
            if log.get_dealer_upcard_points() != log_to_be_checked.get_dealer_upcard_points():
                continue
            # Check for identical dealer action number
            if log.get_action_number() == log_to_be_checked.get_action_number():
                # Assumes player score and dealer upcard points are identical
                found_identical_log = True
                break
        return found_identical_log
    
    def insert_log_into_lb_hard_total_memory_matrix(self, log: LbRoundLog, total_winnings: int):
        """
        Adds a win/loss/draw to trial and score values of self.lb_hard_total_memory_matrix.
        """
        # Retrieve dicts needed to get x and y coordinates
        player_score_to_index_number_dict = self.hard_total_strategy.PLAYER_SCORE_TO_INDEX
        dealer_upcard_points_to_index_number_dict = self.hard_total_strategy.UPCARD_POINTS_TO_INDEX_NUMBER
        
        # Create coordinate values
        x_coordinate = dealer_upcard_points_to_index_number_dict[log.get_dealer_upcard_points()]
        y_coordinate = player_score_to_index_number_dict[log.get_player_score()]
        z_coordinate = log.get_action_number()
        
        # Record use of action number and its outcome
        # Check for win
        if total_winnings > 0:
            self.lb_hard_total_memory_matrix.award_win(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Check for draw
        if total_winnings == 0:
            self.lb_hard_total_memory_matrix.award_draw(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Check for loss
        if total_winnings < 0:
            self.lb_hard_total_memory_matrix.award_loss(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
    
    def insert_log_into_lb_soft_total_memory_matrix(self, log: LbRoundLog, total_winnings: int):
        """
        Adds a win/loss/draw to trial and score values of self.lb_soft_total_memory_matrix.
        """
        # Retrieve dicts needed to get x and y coordinates
        player_score_to_index_number_dict = self.soft_total_strategy.PLAYER_SCORE_TO_INDEX
        dealer_upcard_points_to_index_number_dict = self.soft_total_strategy.UPCARD_POINTS_TO_INDEX_NUMBER
        
        # Create coordinate values
        x_coordinate = dealer_upcard_points_to_index_number_dict[log.get_dealer_upcard_points()]
        y_coordinate = player_score_to_index_number_dict[log.get_player_score()]
        z_coordinate = log.get_action_number()
        
        # Record use of action number and its outcome
        # Check for win
        if total_winnings > 0:
            self.lb_soft_total_memory_matrix.award_win(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Check for draw
        if total_winnings == 0:
            self.lb_soft_total_memory_matrix.award_draw(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Check for loss
        if total_winnings < 0:
            self.lb_soft_total_memory_matrix.award_loss(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
    
    def insert_log_into_lb_split_pair_memory_matrix(self, log: LbRoundLog, total_winnings: int):
        """
        Adds a win/loss/draw to trial and score values of self.lb_split_pair_memory_matrix.
        """
        # Retrieve dicts needed to get x and y coordinates
        player_score_to_index_number_dict = self.split_pair_strategy.PLAYER_SCORE_TO_INDEX
        dealer_upcard_points_to_index_number_dict = self.split_pair_strategy.UPCARD_POINTS_TO_INDEX_NUMBER
        
        # Create coordinate values
        x_coordinate = dealer_upcard_points_to_index_number_dict[log.get_dealer_upcard_points()]
        y_coordinate = player_score_to_index_number_dict[log.get_player_score()]
        z_coordinate = log.get_action_number()
        
        # Record use of action number and its outcome
        # Check for win
        if total_winnings > 0:
            self.lb_split_pair_memory_matrix.award_win(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Check for draw
        if total_winnings == 0:
            self.lb_split_pair_memory_matrix.award_draw(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
            return
        # Assumes loss
        self.lb_split_pair_memory_matrix.award_loss(x_coordinate=x_coordinate, y_coordinate=y_coordinate, z_coordinate=z_coordinate)
    
    def increment_strategy_matrix_action_numbers(self):
        """
        Iterates through all logs of strategy uses in matrixes and increases the action number by one, 
        or reset to 0 if not incrementable by 1.
        """
        # Update hard_total_strategy_matrix
        for log in self.lb_hard_total_round_logs:
            next_action_number = (log.get_action_number() + 1) % 8
            self.hard_total_strategy.set_action_number(new_action_number=next_action_number, dealer_upcard_points=log.get_dealer_upcard_points(), player_hard_total=log.get_player_score())
        # Update soft_total_strategy_matrix
        for log in self.lb_soft_total_round_logs:
            next_action_number = (log.get_action_number() + 1) % 8
            self.soft_total_strategy.set_action_number(new_action_number=next_action_number, dealer_upcard_points=log.get_dealer_upcard_points(), player_soft_total=log.get_player_score())
        # Update split_pair_strategy_matrix
        for log in self.lb_split_pair_round_logs:
            next_action_number = (log.get_action_number() + 1) % 2
            self.split_pair_strategy.set_action_number(new_action_number=next_action_number, dealer_upcard_points=log.get_dealer_upcard_points(), split_pair_score=log.get_player_score())
    
    def process_all_round_logs(self, total_winnings: int):
        """
        Iterates through all LB round logs and adds them to the corresponding LB memory matrix
        """
        # Update lb_hard_total_memory_matrix
        for log in self.lb_hard_total_round_logs:
            self.insert_log_into_lb_hard_total_memory_matrix(log=log, total_winnings=total_winnings)
        # Update lb_soft_total_memory_matrix
        for log in self.lb_soft_total_round_logs:
            self.insert_log_into_lb_soft_total_memory_matrix(log=log, total_winnings=total_winnings)
        # Update lb_split_pair_memory_matrix
        for log in self.lb_split_pair_round_logs:
            self.insert_log_into_lb_split_pair_memory_matrix(log=log, total_winnings=total_winnings)
    
    def clear_lb_hard_total_memory_matrix(self):
        """
        Resets all trials and points numbers to 0 inside self.lb_hard_total_memory_matrix
        """
        self.lb_hard_total_memory_matrix = LbStrategy(height = 18, depth = 8)
    
    def clear_lb_soft_total_memory_matrix(self):
        """
        Resets all trials and points numbers to 0 inside self.lb_soft_total_memory_matrix
        """
        self.lb_soft_total_memory_matrix = LbStrategy(height = 20, depth = 8)
    
    def clear_lb_split_pair_memory_matrix(self):
        """
        Resets all trials and points numbers to 0 inside self.lb_split_pair_memory_matrix
        """
        self.lb_split_pair_memory_matrix = LbStrategy(height = 10, depth = 2)