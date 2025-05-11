import multiprocessing
import time
import json
import http.client
from urllib.parse import urlparse
from striker.constants import is_my_computer
from striker.shared import SharedValue


from striker.constants import (
    STRIKER_WHO_AM_I,
    STRIKER_VERSION,
    SIMULATIONS_URL,
    NUMBER_OF_HANDS_DATABASE,
    BILLION,
)


#
class Report:
    def __init__(self):
        self.total_rounds = SharedValue("i", 0)  # 'i' is for int
        self.total_hands = SharedValue("i", 0)
        self.total_bet = SharedValue("i", 0)
        self.total_won = SharedValue("i", 0)
        self.total_blackjacks = SharedValue("i", 0)
        self.total_doubles = SharedValue("i", 0)
        self.total_splits = SharedValue("i", 0)
        self.total_splits_ace = SharedValue("i", 0)
        self.total_wins = SharedValue("i", 0)
        self.total_loses = SharedValue("i", 0)
        self.total_pushes = SharedValue("i", 0)

    def init_report(self, parameters):
        self.name = parameters.name
        self.version = STRIKER_VERSION
        self.playbook = parameters.playbook
        self.simulator = STRIKER_WHO_AM_I
        self.strategy = parameters.strategy
        self.total_threads = SharedValue("i", parameters.number_of_threads)
        self.decks = parameters.decks
        self.epoch = parameters.epoch
        self.start = time.time()
        self.end = 0
        self.duration = 0
        self.advantage = 0.0
        self.per_billion = 0.0

    def merge_report(self, b):
        self.total_rounds.inc(b.total_rounds.get())
        self.total_hands.inc(b.total_hands.get())
        self.total_bet.inc(b.total_bet.get())
        self.total_won.inc(b.total_won.get())
        self.total_blackjacks.inc(b.total_blackjacks.get())
        self.total_doubles.inc(b.total_doubles.get())
        self.total_splits.inc(b.total_splits.get())
        self.total_splits_ace.inc(b.total_splits_ace.get())
        self.total_wins.inc(b.total_wins.get())
        self.total_loses.inc(b.total_loses.get())
        self.total_pushes.inc(b.total_pushes.get())

    def finish_report(self):
        self.end = time.time()
        self.duration = self.end - self.start
        self.advantage = (
            (self.total_won.get() / self.total_bet.get()) * 100
            if self.total_bet.get()
            else 0.0
        )
        self.per_billion = (
            (self.duration * BILLION / self.total_hands.get())
            if self.total_hands.get()
            else 0.0
        )

    # Print out the results
    def print_report(self):
        print(f"    {'Number of hands':<26}: {self.total_hands.get():>17,}")
        print(f"    {'Number of rounds':<26}: {self.total_rounds.get():>17,}")
        if self.total_hands.get() == 0:
            return
        average_bet_per_hand = self.total_bet.get() / self.total_hands.get()
        print(
            f"    {'Total bet':<26}: {self.total_bet.get():>17,} {average_bet_per_hand:+08.3f} average bet per hand"
        )
        average_won_per_hand = self.total_won.get() / self.total_hands.get()
        print(
            f"    {'Total won':<26}: {self.total_won.get():>17,} {average_won_per_hand:+08.3f} average won per hand"
        )
        percent_blackjacks_per_hand = (
            self.total_blackjacks.get() / self.total_hands.get() * 100.0
        )
        print(
            f"    {'Number of blackjacks':<26}: {self.total_blackjacks.get():>17,} {percent_blackjacks_per_hand:+08.3f} % of total hands"
        )
        percent_doubles_per_hand = (
            self.total_doubles.get() / self.total_hands.get() * 100.0
        )
        print(
            f"    {'Number of doubles':<26}: {self.total_doubles.get():>17,} {percent_doubles_per_hand:+08.3f} % of total hands"
        )
        percent_splits_per_hand = (
            self.total_splits.get() / self.total_hands.get() * 100.0
        )
        print(
            f"    {'Number of splits':<26}: {self.total_splits.get():>17,} {percent_splits_per_hand:+08.3f} % of total hands"
        )
        percent_splits_ace_per_hand = (
            self.total_splits_ace.get() / self.total_hands.get() * 100.0
        )
        print(
            f"    {'Number of splits - Aces':<26}: {self.total_splits_ace.get():>17,} {percent_splits_ace_per_hand:+08.3f} % of total hands"
        )
        percent_wins_per_hand = self.total_wins.get() / self.total_hands.get() * 100.0
        print(
            f"    {'Number of wins':<26}: {self.total_wins.get():>17,} {percent_wins_per_hand:+08.3f} % of total hands"
        )
        percent_pushes_per_hand = (
            self.total_pushes.get() / self.total_hands.get() * 100.0
        )
        print(
            f"    {'Number of pushes':<26}: {self.total_pushes.get():>17,} {percent_pushes_per_hand:+08.3f} % of total hands"
        )
        percent_loses_per_hand = self.total_loses.get() / self.total_hands.get() * 100.0
        print(
            f"    {'Number of loses':<26}: {self.total_loses.get():>17,} {percent_loses_per_hand:+08.3f} % of total hands"
        )
        print(f"    {'Total time':<26}: {self.duration:>17,.0f} seconds")
        print(f"    {'Number of threads':<26}: {self.total_threads.get():>17,} threads")
        print(
            f"    {'Average time':<26}: {self.per_billion:17,.0f} seconds per {BILLION:,} hands"
        )
        print(f"    {'Player advantage':<26}: {' ':>17} {self.advantage:+08.3f} %")

    # Insert the simulation results into the database.
    def insert_report(self):
        if not is_my_computer():
            print("    This code is restricted to running only on my computer.")
            return
        if self.total_hands.get() < NUMBER_OF_HANDS_DATABASE:
            print(
                f"    Error: Not enough hands played {self.total_hands.get():,}. Minimum required is {NUMBER_OF_HANDS_DATABASE:,}"
            )
            return

        url = f"http://{SIMULATIONS_URL}/{self.simulator}/{self.decks}/{self.strategy}"

        try:
            # Convert the simulation table to JSON
            # json_data = json.dumps(self.__dict__)
            # To get a JSON string:
            json_data = json.dumps(self.to_json_object(), indent=2)

            headers = {"Content-Type": "application/json"}

            # Parse the URL
            parsed_url = urlparse(url)
            connection = http.client.HTTPConnection(parsed_url.netloc)

            # Send the POST request
            connection.request("POST", parsed_url.path, body=json_data, headers=headers)

            # Get the response
            response = connection.getresponse()
            response_data = response.read().decode()

            # Close the connection
            connection.close()

            # Handle the response
            if response.status != 200:
                print(
                    f"    Error inserting into Simulation table. Status: {response.status}"
                )
                print(f"    Response: {response_data}")
            else:
                print(f"    Simulation inserted successfully.")

        except Exception as e:
            print(f"    Error sending request: {e}")

    def to_json_object(self):
        return {
            "guid": self.name,
            "version": self.version,
            "simulator": self.simulator,
            "threads": self.total_threads.get(),
            "playbook": self.playbook,
            "decks": self.decks,
            "strategy": self.strategy,
            "rounds": self.total_rounds.get(),
            "hands": self.total_hands.get(),
            "total_bet": self.total_bet.get(),
            "total_won": self.total_won.get(),
            "total_blackjacks": self.total_blackjacks.get(),
            "total_doubles": self.total_doubles.get(),
            "total_splits": self.total_splits.get(),
            "total_splits_ace": self.total_splits_ace.get(),
            "total_wins": self.total_wins.get(),
            "total_loses": self.total_loses.get(),
            "total_pushes": self.total_pushes.get(),
            "advantage": self.advantage,
            "epoch": self.epoch,
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "per_billion": self.per_billion,
        }
