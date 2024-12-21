import time

#
class Report:
    def __init__(self):
        self.total_rounds = 0
        self.total_hands = 0
        self.total_blackjacks = 0
        self.total_doubles = 0
        self.total_splits = 0
        self.total_wins = 0
        self.total_loses = 0
        self.total_pushes = 0
        self.total_bet = 0
        self.total_won = 0
        self.start = time.time()
        self.end = 0
        self.duration = 0

