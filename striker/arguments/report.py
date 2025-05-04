import time
import json
import http.client
from urllib.parse import urlparse


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
        self.total_rounds = 0
        self.total_hands = 0
        self.total_bet = 0
        self.total_won = 0
        self.total_blackjacks = 0
        self.total_doubles = 0
        self.total_splits = 0
        self.total_splits_ace = 0
        self.total_wins = 0
        self.total_loses = 0
        self.total_pushes = 0
        self.total_threads = 1

    def init_report(self, parameters):
        self.name = parameters.name
        self.version = STRIKER_VERSION
        self.playbook = parameters.playbook
        self.simulator = STRIKER_WHO_AM_I
        self.strategy = parameters.strategy
        self.decks = parameters.decks
        self.epoch = parameters.epoch
        self.start = time.time()
        self.end = 0
        self.duration = 0
        self.advantage = 0.0
        self.per_billion = 0.0

    def merge_report(self, b):
        self.total_rounds += b.total_rounds
        self.total_hands += b.total_hands
        self.total_bet += b.total_bet
        self.total_won += b.total_won
        self.total_blackjacks += b.total_blackjacks
        self.total_doubles += b.total_doubles
        self.total_splits += b.total_splits
        self.total_splits_ace += b.total_splits_ace
        self.total_wins += b.total_wins
        self.total_loses += b.total_loses
        self.total_pushes += b.total_pushes

    def finish_report(self):
        self.end = time.time()
        self.duration = self.end - self.start
        self.advantage = (
            (self.total_won / self.total_bet) * 100 if self.total_bet else 0.0
        )
        self.per_billion = (
            (self.duration * BILLION / self.total_hands) if self.total_hands else 0.0
        )

    # Print out the results
    def print_report(self):
        print(f"    {'Number of hands':<26}: {self.total_hands:>17,}")
        print(f"    {'Number of rounds':<26}: {self.total_rounds:>17,}")
        if self.total_hands == 0:
            return
        average_bet_per_hand = self.total_bet / self.total_hands
        print(
            f"    {'Total bet':<26}: {self.total_bet:>17,} {average_bet_per_hand:+08.3f} average bet per hand"
        )
        average_won_per_hand = self.total_won / self.total_hands
        print(
            f"    {'Total won':<26}: {self.total_won:>17,} {average_won_per_hand:+08.3f} average won per hand"
        )
        percent_blackjacks_per_hand = self.total_blackjacks / self.total_hands * 100.0
        print(
            f"    {'Number of blackjacks':<26}: {self.total_blackjacks:>17,} {percent_blackjacks_per_hand:+08.3f} % of total hands"
        )
        percent_doubles_per_hand = self.total_doubles / self.total_hands * 100.0
        print(
            f"    {'Number of doubles':<26}: {self.total_doubles:>17,} {percent_doubles_per_hand:+08.3f} % of total hands"
        )
        percent_splits_per_hand = self.total_splits / self.total_hands * 100.0
        print(
            f"    {'Number of splits':<26}: {self.total_splits:>17,} {percent_splits_per_hand:+08.3f} % of total hands"
        )
        percent_splits_ace_per_hand = self.total_splits_ace / self.total_hands * 100.0
        print(
            f"    {'Number of splits - Aces':<26}: {self.total_splits_ace:>17,} {percent_splits_ace_per_hand:+08.3f} % of total hands"
        )
        percent_wins_per_hand = self.total_wins / self.total_hands * 100.0
        print(
            f"    {'Number of wins':<26}: {self.total_wins:>17,} {percent_wins_per_hand:+08.3f} % of total hands"
        )
        percent_pushes_per_hand = self.total_pushes / self.total_hands * 100.0
        print(
            f"    {'Number of pushes':<26}: {self.total_pushes:>17,} {percent_pushes_per_hand:+08.3f} % of total hands"
        )
        percent_loses_per_hand = self.total_loses / self.total_hands * 100.0
        print(
            f"    {'Number of loses':<26}: {self.total_loses:>17,} {percent_loses_per_hand:+08.3f} % of total hands"
        )
        print(f"    {'Total time':<26}: {self.duration:>17,.0f} seconds")
        print(f"    {'Number of threads':<26}: {self.total_threads:>17,} threads")
        print(
            f"    {'Average time':<26}: {self.per_billion:17,.0f} seconds per {BILLION:,} hands"
        )
        print(f"    {'Player advantage':<26}: {' ':>17} {self.advantage:+08.3f} %")

    # Insert the simulation results into the database.
    def insert_report(self):
        if self.total_hands < NUMBER_OF_HANDS_DATABASE:
            print(
                f"    Error: Not enough hands played {self.total_hands:,}. Minimum required is {NUMBER_OF_HANDS_DATABASE:,}"
            )
            return

        url = f"http://{SIMULATIONS_URL}/{self.simulator}/{self.decks}/{self.strategy}"
        print(url)

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
            "threads": self.total_threads,
            "playbook": self.playbook,
            "decks": self.decks,
            "strategy": self.strategy,
            "rounds": self.total_rounds,
            "hands": self.total_hands,
            "total_bet": self.total_bet,
            "total_won": self.total_won,
            "total_blackjacks": self.total_blackjacks,
            "total_doubles": self.total_doubles,
            "total_splits": self.total_splits,
            "total_splits_ace": self.total_splits_ace,
            "total_wins": self.total_wins,
            "total_loses": self.total_loses,
            "total_pushes": self.total_pushes,
            "advantage": self.advantage,
            "epoch": self.epoch,
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "per_billion": self.per_billion,
        }
