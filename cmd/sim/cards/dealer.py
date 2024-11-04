from sim.cards import Hand

class Dealer:
    def __init__(self, hit_soft_17):
        self.hand = Hand()  # Assuming Hand class is defined elsewhere
        self.hit_soft_17 = hit_soft_17

    def reset(self):
        self.hand.reset()

    def stand(self):
        if self.hit_soft_17 and self.hand.soft_17():
            return False
        return self.hand.total() >= 17

    def draw(self, card):
        return self.hand.draw(card)

