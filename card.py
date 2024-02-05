class Card(object):
    """"
    Attributes: \n
        - self.rank(str): Value of card. Example: "Ace"\n
        - self.suit(str): Suit type of card. Example: "Spades"\n
        - self.points(int): Point value of card.\n
            - Example: Card rank of "Jack" is assigned 10 points in Blackjack 
    """
    def __init__(self, rank: str, suit: str, points: int, visible: bool = False):
        self.rank = rank
        self.suit = suit
        self.points = points
        self.visible = visible
    
    def make_visible(self):
        self.visible = True
    
    def full_name(self) -> str:
        """
        Returns the full name of a card, for example: \n
        "Ace of Spades"
        """
        return f'{self.rank} of {self.suit}'
    