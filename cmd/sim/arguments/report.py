#import json
import time
#import uuid
#import requests
#from io import BytesIO

#
class Report:
    def __init__(self):
        self.total_rounds = 0
        self.total_hands = 0
        self.total_bet = 0
        self.total_won = 0
        self.start = time.time()
        self.end = 0
        self.duration = 0

