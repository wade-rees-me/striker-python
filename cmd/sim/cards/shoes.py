import random
from .cards import Card
from .decks import Deck

class Shoe:
    def __init__(self, deck, number_of_decks, penetration):
        """
        Initializes a Shoe object for handling multiple decks of cards.
        :param deck: A Deck object containing the cards
        :param number_of_decks: The number of decks to use in the shoe
        :param penetration: The penetration point (where to cut the deck)
        """
        self.cards = []
        self.inplay = []
        self.discards = []
        self.downcard = None
        self.force_shuffle = False
        self.number_of_decks = number_of_decks
        self.number_of_cards = 0
        self.cut_card = 0
        self.number_of_shuffles = 0
        self.number_out_of_cards = 0

        # Add cards to the shoe
        for _ in range(self.number_of_decks):
            self.discards.extend(deck.cards)

        self.number_of_cards = len(self.discards)
        self.cut_card = int(self.number_of_cards * penetration)

        # Set index for each card in the shoe
        for i in range(self.number_of_cards):
            self.discards[i].index = i

    def shuffle(self):
        """
        Shuffles the shoe and resets the necessary fields.
        """
        self.discards.extend(self.cards)
        self.discards.extend(self.inplay)
        self.cards = []
        self.inplay = []
        self.force_shuffle = False
        self._shuffle_discards_fisher_yates()

    def shuffle_discards(self):
        """
        Forces a shuffle of the discards.
        """
        self.force_shuffle = True
        self.number_out_of_cards += 1
        self._shuffle_discards_fisher_yates()

    def _shuffle_discards_fisher_yates(self):
        """
        Shuffles the discards using the Fisher-Yates algorithm.
        """
        random.shuffle(self.discards)
        self.cards = self.discards[:]
        self.discards = []
        self.discard(self.draw())  # Burn a card
        self.number_of_shuffles += 1

    def should_shuffle(self):
        """
        Determines if the shoe should be shuffled based on the number of cards left.
        """
        self.discards.extend(self.inplay)
        self.inplay = []
        return len(self.cards) < (self.number_of_cards - self.cut_card) or self.force_shuffle

    def draw(self):
        """
        Draws a card from the shoe. Shuffles if necessary.
        :return: The drawn Card object.
        """
        if not self.cards:
            self.shuffle_discards()
            if not self.cards:
                raise Exception("shuffle discards")

        card = self.cards.pop(0)
        self.inplay.append(card)
        return card

    def discard(self, card):
        """
        Discards a card, moving it from in-play to the discard pile.
        :param card: The Card object to be discarded.
        """
        self.discards.append(card)
        self.inplay = [c for c in self.inplay if c != card]

