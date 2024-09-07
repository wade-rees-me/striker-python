from sim.cards import Hand

class Dealer:
    def __init__(self, hit_soft_17):
        """
        Initializes a Dealer object.
        :param hit_soft_17: A boolean indicating if the dealer should hit on soft 17.
        """
        self.hand = Hand()  # Assuming Hand class is defined elsewhere
        self.hit_soft_17 = hit_soft_17

    def reset(self):
        """
        Resets the dealer's hand.
        """
        self.hand.reset()

    def play(self, shoe):
        """
        Simulates the dealer's play by drawing cards from the shoe until standing.
        :param shoe: Shoe object from which to draw cards.
        """
        while not self.stand():
            self.draw(shoe.draw())

    def stand(self):
        """
        Determines whether the dealer should stand or continue drawing cards.
        :return: True if the dealer should stand, False otherwise.
        """
        if self.hit_soft_17 and self.hand.soft_17():
            return False
        return self.hand.total() >= 17

    def draw(self, card):
        """
        Draws a card and adds it to the dealer's hand.
        :param card: Card object to be drawn.
        :return: The drawn card.
        """
        return self.hand.draw(card)

