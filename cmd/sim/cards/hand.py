class Hand:
    def __init__(self):
        """
        Initializes a new Hand object.
        :attribute cards: List of Card objects in the hand.
        :attribute hand_total: Total value of the hand.
        :attribute soft_ace: Number of aces valued as 11.
        :attribute surrender: Whether the player has surrendered.
        """
        self.cards = []
        self.hand_total = 0
        self.soft_ace = 0
        self.surrender = False

    def reset(self):
        """
        Resets the hand.
        """
        self.cards = []
        self.hand_total = 0
        self.soft_ace = 0
        self.surrender = False

    def draw(self, card):
        """
        Adds a card to the hand and updates the hand total.
        :param card: Card object to be added.
        :return: The drawn Card object.
        """
        self.cards.append(card)
        self.total_hand()
        return card

    def blackjack(self):
        """
        Checks if the hand is a Blackjack (two cards, total 21).
        :return: True if Blackjack, False otherwise.
        """
        return len(self.cards) == 2 and self.hand_total == 21

    def pair(self):
        """
        Checks if the hand is a pair (two cards of the same rank).
        :return: True if the cards form a pair, False otherwise.
        """
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def pair_of_aces(self):
        """
        Checks if the hand is a pair of aces.
        :return: True if both cards are aces, False otherwise.
        """
        return self.pair() and self.cards[0].rank == "ace"

    def busted(self):
        """
        Checks if the hand has busted (total > 21).
        :return: True if the hand is busted, False otherwise.
        """
        return self.hand_total > 21

    def soft(self):
        """
        Checks if the hand has a soft ace (an ace valued as 11).
        :return: True if the hand contains a soft ace, False otherwise.
        """
        return self.soft_ace > 0

    def total(self):
        """
        Returns the total value of the hand.
        :return: The total value of the hand.
        """
        return self.hand_total

    def soft_17(self):
        """
        Checks if the hand is a soft 17 (total is 17 with a soft ace).
        :return: True if the hand is a soft 17, False otherwise.
        """
        return self.total() == 17 and self.soft()

    def split_pair(self):
        """
        Splits the hand if it's a pair and returns the second card.
        :return: The second Card object in the pair.
        :raises: Exception if trying to split a non-pair.
        """
        if self.pair():
            card = self.cards[1]
            self.cards = self.cards[:1]
            self.total_hand()
            return card
        raise Exception("Trying to split a non-pair")

    def total_hand(self):
        """
        Recalculates the total value of the hand, accounting for soft aces.
        """
        self.hand_total = 0
        self.soft_ace = 0

        # Calculate the total value and count soft aces
        for card in self.cards:
            self.hand_total += card.value
            if card.value == 11:
                self.soft_ace += 1

        # Adjust for soft aces if hand total exceeds 21
        while self.hand_total > 21 and self.soft_ace > 0:
            self.hand_total -= 10
            self.soft_ace -= 1

