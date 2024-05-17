
class LbRoundLog(object):
    """
    LbRoundLogs are objects that log the use of a specific action number in strategy matrixes before a round 
    has concluded.
    """
    
    def __init__(self, player_score : int, dealer_upcard_points: int, action_number: int) -> None:
        self._player_score = player_score
        self._dealer_upcard_points = dealer_upcard_points
        self._action_number = action_number
    
    def get_player_score(self) -> int:
        """
        Returns the player's score.
        """
        return self._player_score

    def get_dealer_upcard_points(self) -> int:
        """
        Returns the dealer's upcard points.
        """
        return self._dealer_upcard_points

    def get_action_number(self) -> int:
        """
        Returns the action number.
        """
        return self._action_number