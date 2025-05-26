import multiprocessing
import time
import json
from striker.constants import STRIKER_WHO_AM_I, STRIKER_VERSION
from striker.shared import SharedValue


def generate_name():
    t = time.localtime()  # Get the current time
    # Format the name with the current date and time as part of the string
    name = f"{STRIKER_WHO_AM_I}_{t.tm_year:04d}_{t.tm_mon:02d}_{t.tm_mday:02d}_{int(time.time()):012d}"
    return name


#
class Parameters:
    def __init__(self, arguments):
        self.name = generate_name()
        self.playbook = f"{arguments.get_decks()}-{arguments.get_strategy()}"
        self.processor = STRIKER_WHO_AM_I
        self.epoch = self.get_current_time()
        self.strategy = arguments.get_strategy()
        self.decks = arguments.get_decks()
        self.number_of_decks = arguments.get_number_of_decks()
        self.number_of_hands = SharedValue("i", arguments.number_of_hands)
        self.number_of_threads = SharedValue("i", arguments.number_of_threads)
        self.share_of_hands = SharedValue(
            "i", (self.number_of_hands.get() / self.number_of_threads.get()) + 1
        )
        self.verbose = self.number_of_threads.get() == 1

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def print(self):
        print(f"    {'Processor':<26}: {self.processor}")
        print(f"    {'Threads':<26}: {self.number_of_threads}")
        print(f"    {'Name':<26}: {self.name}")
        print(f"    {'Version':<26}: {STRIKER_VERSION}")
        print(f"    {'Playbook':<26}: {self.playbook}")
        print(f"    {'Decks':<26}: {self.decks}")
        print(f"    {'Strategy':<26}: {self.strategy}")
        print(f"    {'Number of hands':<26}: {self.number_of_hands.get():>17,}")
        print(f"    {'Thread share of hands':<26}: {self.share_of_hands.get():>17,}")
        print(f"    {'Epoch':<26}: {self.epoch}")
