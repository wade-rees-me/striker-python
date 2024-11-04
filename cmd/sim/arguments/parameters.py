import time
import json
from sim.constants import STRIKER_WHO_AM_I, STRIKER_VERSION

def generate_name():
    t = time.localtime()  # Get the current time
    # Format the name with the current date and time as part of the string
    name = f"{STRIKER_WHO_AM_I}_{t.tm_year:04d}_{t.tm_mon:02d}_{t.tm_mday:02d}_{int(time.time()):012d}"
    return name

#
class Parameters:
    def __init__(self, decks, strategy, number_of_decks, number_of_hands):
        self.name = generate_name()
        self.decks = decks
        self.strategy = strategy
        self.number_of_decks = number_of_decks
        self.number_of_hands = number_of_hands
        self.playbook = f"{decks}-{strategy}"
        self.processor = STRIKER_WHO_AM_I
        self.timestamp = self.get_current_time()

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def print(self):
        print(f"    {'Name':<24}: {self.name}")
        print(f"    {'Playbook':<24}: {self.playbook}")
        print(f"    {'Processor':<24}: {self.processor}")
        print(f"    {'Version':<24}: {STRIKER_VERSION}")
        print(f"    {'Number of hands':<24}: {self.number_of_hands:,}")
        print(f"    {'Timestamp':<24}: {self.timestamp}")

    def serialize(self):
        data = {
            "playbook": self.playbook,
            "name": self.name,
            "processor": self.processor,
            "timestamp": self.timestamp,
            "decks": self.decks,
            "strategy": self.strategy,
            "number_of_hands": self.number_of_hands,
            "number_of_decks": self.number_of_decks
            #"hit_soft_17": str(self.rules.hit_soft_17).lower(),
            #"surrender": str(self.rules.surrender).lower(),
            #"double_any_two_cards": str(self.rules.double_any_two_cards).lower(),
            #"double_after_split": str(self.rules.double_after_split).lower(),
            #"resplit_aces": str(self.rules.resplit_aces).lower(),
            #"hit_split_aces": str(self.rules.hit_split_aces).lower(),
            #"blackjack_bets": self.rules.blackjack_bets,
            #"blackjack_pays": self.rules.blackjack_pays,
            #"penetration": self.rules.penetration
        }
        return json.dumps(data, indent=4)

