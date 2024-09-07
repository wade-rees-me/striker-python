class Card:
    def __init__(self, suit, rank, value, offset):
        """
        Initializes a new Card object.
        :param suit: Suit of the card (e.g., "hearts")
        :param rank: Rank of the card (e.g., "ace")
        :param value: Value of the card for game calculations
        :param offset: Index of the card in a suit
        """
        self.suit = suit
        self.rank = rank
        self.value = value
        self.offset = offset
        self.index = None  # Index will be set later if needed

    def is_blackjack_ace(self):
        """
        Checks if the card is an Ace in Blackjack (value is 11).
        :return: True if the card is an Ace with value 11, False otherwise.
        """
        return self.value == 11

# Factory function for creating a new Card
def new_card(suit, rank, value, offset):
    """
    Creates and returns a new Card object.
    :param suit: Suit of the card (e.g., "hearts")
    :param rank: Rank of the card (e.g., "ace")
    :param value: Value of the card for game calculations
    :param offset: Index of the card in a suit
    :return: Card object
    """
    return Card(suit, rank, value, offset)

