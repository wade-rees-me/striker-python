from .hand import Hand

class Wager:
    def __init__(self):
        """
        Initializes a Wager object with default values.
        """
        self.hand = Hand()  # Assuming Hand class is defined elsewhere
        self.amount_bet = 0
        self.amount_won = 0
        self.double_bet = 0
        self.double_won = 0
        self.insurance_bet = 0
        self.insurance_won = 0

    def split_wager(self, split):
        """
        Splits the current wager into a new wager.
        :param split: Wager object to split into
        """
        split.reset()
        split.amount_bet = self.amount_bet
        split.hand.draw(self.hand.split_pair())

    def reset(self):
        """
        Resets the wager's values.
        """
        self.hand.reset()
        self.amount_bet = 0
        self.amount_won = 0
        self.double_bet = 0
        self.double_won = 0
        self.insurance_bet = 0
        self.insurance_won = 0

    def bet(self, b):
        """
        Places a bet and checks that it is a multiple of 2.
        :param b: The bet amount
        :raises: ValueError if the bet is not a multiple of 2
        """
        if b % 2 != 0:
            raise ValueError("All bets must be in multiples of 2.")
        self.amount_bet = b

    def double(self):
        """
        Doubles the current bet.
        """
        self.double_bet = self.amount_bet

    def blackjack(self):
        """
        Checks if the associated hand is a Blackjack.
        :return: True if the hand is a Blackjack, False otherwise
        """
        return self.hand.blackjack()

    def won_blackjack(self, pays, bet):
        """
        Calculates the amount won from a Blackjack.
        :param pays: The payout ratio for Blackjack
        :param bet: The initial bet
        """
        self.amount_won = (self.amount_bet * pays) // bet

    def won(self):
        """
        Marks the wager as won.
        """
        self.amount_won = self.amount_bet
        self.double_won = self.double_bet

    def lost(self):
        """
        Marks the wager as lost.
        """
        self.amount_won = -self.amount_bet
        self.double_won = -self.double_bet

    def push(self):
        """
        Pushes the wager (no win or loss).
        """
        pass

    def won_insurance(self):
        """
        Marks the insurance bet as won.
        """
        self.insurance_won = self.insurance_bet * 2

    def lost_insurance(self):
        """
        Marks the insurance bet as lost.
        """
        self.insurance_won = -self.insurance_bet

