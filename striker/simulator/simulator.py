import json
import http.client
import time
from datetime import datetime, timezone
import uuid
from io import BytesIO
from urllib.parse import urlparse
from striker.arguments import Parameters, Report
from striker.constants import STRIKER_WHO_AM_I, SIMULATION_URL, DATABASE_NUMBER_OF_HANDS
from striker.table import Rules
from .table import Table
from .player import Player

# Initialize a DatabaseTable for storing results.
class DatabaseTable:
    def __init__(self, playbook, guid, simulator, simulations, rounds, hands, total_bet, total_won, total_time, average_time, advantage, timestamp, parameters, rules, payload):
        self.playbook = playbook
        self.guid = guid
        self.simulator = simulator
        self.simulations = simulations
        self.rounds = rounds
        self.hands = hands
        self.total_bet = total_bet
        self.total_won = total_won
        self.total_time = total_time
        self.average_time = average_time
        self.advantage = advantage
        self.summary = "no"
        self.timestamp = timestamp
        self.parameters = parameters
        self.rules = rules
        self.payload = payload

class Simulator:
    # Initialize a Simulation object with the provided parameters.
    def __init__(self, parameters, rules, strategy):
        current_time = time.time()
        local_time = time.localtime(current_time)
        self.year = local_time.tm_year
        self.month = local_time.tm_mon
        self.day = local_time.tm_mday
        self.name = f"striker-python_{self.year:4d}_{self.month:02d}_{self.day:02d}_{int(current_time)}"
        self.guid = str(uuid.uuid4())
        self.parameters = parameters
        self.rules = rules
        self.strategy = strategy
        self.table_list = []

        # Initialize tables and players
        table = Table(1, parameters, rules)
        player = Player(parameters, rules, strategy, table.shoe.number_of_cards)
        table.add_player(player)
        self.table_list.append(table)

        self.report = Report()

    # Run the simulation by starting sessions for all tables.
    def run_simulation(self):
        for table in self.table_list:
            print("    Start: " + self.parameters.strategy + " table session");
            table.session(self.parameters.strategy == "mimic")
            print("    End: table session");

        # Merge the results from all tables into one report
        for table in self.table_list:
            self.report.total_rounds += table.report.total_rounds
            self.report.total_hands += table.report.total_hands
            self.report.total_blackjacks += table.player.report.total_blackjacks
            self.report.total_doubles += table.player.report.total_doubles
            self.report.total_splits += table.player.report.total_splits
            self.report.total_wins += table.player.report.total_wins
            self.report.total_pushes += table.player.report.total_pushes
            self.report.total_loses += table.player.report.total_loses
            self.report.total_bet += table.player.report.total_bet
            self.report.total_won += table.player.report.total_won
            self.report.duration += table.report.duration

    # Process the simulation and prepare a database entry for the results.
    def run_simulation_process(self):
        print(f"  Start: simulation {self.parameters.name}");
        self.run_simulation()
        print(f"  End: simulation");

        tbs = DatabaseTable(
            playbook=self.parameters.playbook,
            guid=self.parameters.name,
            simulator=STRIKER_WHO_AM_I,
            simulations="1",
            rounds=str(self.report.total_rounds),
            hands=str(self.report.total_hands),
            total_bet=str(self.report.total_bet),
            total_won=str(self.report.total_won),
            total_time=str(int(self.report.duration)),
            average_time=f"{(self.report.duration / self.report.total_hands) * 1e6:.2f} seconds",
            advantage=f"{(self.report.total_won / self.report.total_bet) * 100:+04.3f} %",
            timestamp = self.parameters.timestamp,
            parameters = self.parameters.serialize(),
            rules = self.rules.serialize(),
            payload = "n/a"#json.dumps(self.report.__dict__)
        )

        self.print_simulation_report(tbs)

        # Check if total hands exceed the threshold
        if self.report.total_hands >= DATABASE_NUMBER_OF_HANDS:
            self.insert_simulation_table(tbs)

    def print_simulation_report(self, tbs):
        # Print out the results
        print("\n  -- results ---------------------------------------------------------------------")
        print(f"    {'Number of hands':<24}: {self.report.total_hands:,}")
        print(f"    {'Number of rounds':<24}: {self.report.total_rounds:,}")
        average_bet_per_hand = self.report.total_bet / self.report.total_hands
        print(f"    {'Total bet':<24}: {self.report.total_bet:,} {average_bet_per_hand:+04.3f} average bet per hand")
        average_won_per_hand = self.report.total_won / self.report.total_hands
        print(f"    {'Total won':<24}: {self.report.total_won:,} {average_won_per_hand:+04.3f} average won per hand")

        percent_blackjacks_per_hand = self.report.total_blackjacks / self.report.total_hands * 100.0
        print(f"    {'Total blackjacks':<24}: {self.report.total_blackjacks:,} {percent_blackjacks_per_hand:+04.3f} percent of total hands")
        percent_doubles_per_hand = self.report.total_doubles / self.report.total_hands * 100.0
        print(f"    {'Total doubles':<24}: {self.report.total_doubles:,} {percent_doubles_per_hand:+04.3f} percent of total hands")
        percent_splits_per_hand = self.report.total_splits / self.report.total_hands * 100.0
        print(f"    {'Total splits':<24}: {self.report.total_splits:,} {percent_splits_per_hand:+04.3f} percent of total hands")
        percent_wins_per_hand = self.report.total_wins / self.report.total_hands * 100.0
        print(f"    {'Total wins':<24}: {self.report.total_wins:,} {percent_wins_per_hand:+04.3f} percent of total hands")
        percent_pushes_per_hand = self.report.total_pushes / self.report.total_hands * 100.0
        print(f"    {'Total pushes':<24}: {self.report.total_pushes:,} {percent_pushes_per_hand:+04.3f} percent of total hands")
        percent_loses_per_hand = self.report.total_loses / self.report.total_hands * 100.0
        print(f"    {'Total loses':<24}: {self.report.total_loses:,} {percent_loses_per_hand:+04.3f} percent of total hands")

        print(f"    {'Total time':<24}: {self.report.duration:,} seconds")
        print(f"    {'Average time':<24}: {tbs.average_time} seconds per 1,000,000 hands")
        print(f"    {'Player advantage':<24}: {tbs.advantage}")
        print("  --------------------------------------------------------------------------------\n")

    # Insert the simulation results into the database.
    def insert_simulation_table(self, simulation_table):
        url = f"http://{SIMULATION_URL}/{simulation_table.simulator}/{simulation_table.playbook}/{simulation_table.guid}"
        print(f"  -- insert ----------------------------------------------------------------------");
        print(f"Inserting Simulation: {url}")

        try:
            # Convert the simulation table to JSON
            json_data = json.dumps(simulation_table.__dict__)
            headers = {"Content-Type": "application/json"}

            # Parse the URL
            parsed_url = urlparse(url)
            connection = http.client.HTTPConnection(parsed_url.netloc)

            # Send the POST request
            connection.request("POST", parsed_url.path, body=json_data, headers=headers)

            # Get the response
            response = connection.getresponse()
            response_data = response.read().decode()

            print("Status:", response.status)
            print("Response:", response_data)

            # Close the connection
            connection.close()

            # Handle the response
            if response.status != 200:
                print(f"Error inserting into Simulation table. Status: {response.status_code}")
                print(f"Response: {response_data}")
            else:
                print(f"Simulation inserted successfully. Response: {response_data}")

        except Exception as e:
            print(f"Error sending request: {e}")

        print("  --------------------------------------------------------------------------------\n")

