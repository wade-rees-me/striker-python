class Card:
    def __init__(self, suit, rank, value, offset):
        self.suit = suit
        self.rank = rank
        self.value = value
        self.offset = offset
        self.index = None  # Index will be set later if needed

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_value(self):
        return self.value

    def get_offset(self):
        return self.offset

    def is_blackjack_ace(self):
        return self.value == 11

# Factory function for creating a new Card
def new_card(suit, rank, value, offset):
    return Card(suit, rank, value, offset)

