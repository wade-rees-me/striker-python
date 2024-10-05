from .hand import Hand

MINIMUM_BET = 2
MAXIMUM_BET = 98

class Wager:
    def __init__(self):
        self.hand = Hand()  # Assuming Hand class is defined elsewhere
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
        self.amount_bet = (min(MAXIMUM_BET, max(MINIMUM_BET, bet)) + 1) // 2 * 2;
        #print(f"bet: {bet} = {self.amount_bet}")

    def double(self):
        self.amount_bet = self.amount_bet * 2
        #print(f"double: {self.amount_bet}")

    def blackjack(self):
        return self.hand.blackjack()

    def won_blackjack(self, pays, bet):
        self.amount_won = (self.amount_bet * pays) // bet
        #print(f"blackjack: {self.amount_won}")

    def won(self):
        self.amount_won = self.amount_bet
        #print(f"won: {self.amount_won}")

    def lost(self):
        self.amount_won = -self.amount_bet
        #print(f"lost: {self.amount_won}")

    def push(self):
        pass

    def won_insurance(self):
        self.insurance_won = self.insurance_bet * 2

    def lost_insurance(self):
        self.insurance_won = -self.insurance_bet

