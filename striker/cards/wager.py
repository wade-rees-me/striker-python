from .hand import Hand

class Wager:
    def __init__(self, minimum_bet, maximum_bet):
        self.hand = Hand()  # Assuming Hand class is defined elsewhere
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        self.amount_bet = 0
        self.amount_won = 0
        self.insurance_bet = 0
        self.insurance_won = 0

    def split_wager(self, split):
        split.reset()
        split.amount_bet = self.amount_bet
        split.hand.draw(self.hand.split_pair())

    def reset(self):
        self.hand.reset()
        self.amount_bet = 0
        self.amount_won = 0
        self.insurance_bet = 0
        self.insurance_won = 0

    def bet(self, bet):
        self.amount_bet = (min(self.maximum_bet, max(self.minimum_bet, bet)) + 1) // 2 * 2;

    def double(self):
        self.amount_bet = self.amount_bet * 2

    def blackjack(self):
        return self.hand.blackjack()

    def won_blackjack(self, pays, bet):
        self.amount_won = (self.amount_bet * pays) // bet

    def won(self):
        self.amount_won = self.amount_bet

    def lost(self):
        self.amount_won = -self.amount_bet

    def push(self):
        pass

    def won_insurance(self):
        self.insurance_won = self.insurance_bet * 2

    def lost_insurance(self):
        self.insurance_won = -self.insurance_bet

