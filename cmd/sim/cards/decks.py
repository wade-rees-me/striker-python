from .cards import Card, new_card

class Deck:
    def __init__(self):
        """
        Initializes a new Deck object.
        :attribute cards: List of Card objects in the deck.
        """
        self.cards = []

# Dictionary to store poker card ranks, values, and offsets
poker_cards = {
    "two": [2, 0],
    "three": [3, 1],
    "four": [4, 2],
    "five": [5, 3],
    "six": [6, 4],
    "seven": [7, 5],
    "eight": [8, 6],
    "nine": [9, 7],
    "ten": [10, 8],
    "jack": [10, 9],
    "queen": [10, 10],
    "king": [10, 11],
    "ace": [11, 12],
}

# List of suits
suits = ["spades", "diamond", "clubs", "hearts"]

# Global variable for deck of poker cards
deck_of_poker_cards = None

# Function to create a new deck
def new_deck(suits, ranks, copies):
    """
    Creates a new Deck object with specified number of copies of cards.
    
    :param suits: List of suits (e.g., "spades", "hearts")
    :param ranks: Dictionary of card ranks, values, and offsets
    :param copies: Number of copies of the deck to create
    :return: A new Deck object
    """
    deck = Deck()
    for _ in range(copies):
        for suit in suits:
            for rank, value in ranks.items():
                card = new_card(suit, rank, value[0], value[1])
                deck.cards.append(card)
    return deck

# Initialize the deck of poker cards
def init():
    """
    Initializes the global deck_of_poker_cards variable with a standard deck.
    """
    global deck_of_poker_cards
    deck_of_poker_cards = new_deck(suits, poker_cards, 1)

# Run the initialization
init()

