import json
import time
from datetime import datetime, timezone
import uuid
import threading
import requests
from io import BytesIO
from sim.arguments import Parameters, Report
from sim.constants import STRIKER_WHO_AM_I, SIMULATION_URL, DATABASE_NUMBER_OF_HANDS
from sim.table import Rules
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
    def __init__(self, parameters):
        current_time = time.time()
        local_time = time.localtime(current_time)
        self.year = local_time.tm_year
        self.month = local_time.tm_mon
        self.day = local_time.tm_mday
        self.name = f"striker-python_{self.year:4d}_{self.month:02d}_{self.day:02d}_{int(current_time)}"
        self.guid = str(uuid.uuid4())
        self.parameters = parameters
        self.table_list = []

        # Initialize tables and players
        table = Table(1, parameters)
        player = Player(parameters, table.shoe.number_of_cards)
        table.add_player(player)
        self.table_list.append(table)

        self.report = Report()

    # Run the simulation by starting sessions for all tables.
    def run_simulation(self):
        threads = []
        for table in self.table_list:
            self.parameters.logger.simulation("    Start: " + self.parameters.strategy + " table session\n");
            table.session(self.parameters.strategy == "mimic")
            self.parameters.logger.simulation("    End: table session\n");
            #if self.parameters.strategy == "mimic":
                #thread = threading.Thread(target=table.session_mimic)
            #else:
                #thread = threading.Thread(target=table.session)
            #threads.append(thread)
            #thread.start()

        # Wait for all threads to finish
        #for thread in threads:
            #thread.join()

        # Merge the results from all tables into one report
        for table in self.table_list:
            self.report.total_rounds += table.report.total_rounds
            self.report.total_hands += table.report.total_hands
            self.report.total_bet += table.player.report.total_bet
            self.report.total_won += table.player.report.total_won
            self.report.duration += table.report.duration

    # Process the simulation and prepare a database entry for the results.
    def run_simulation_process(self):
        self.parameters.logger.simulation(f"  Start: simulation {self.parameters.name}\n");
        self.run_simulation()
        self.parameters.logger.simulation(f"  End: simulation\n");

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
            average_time=f"{(self.report.duration / self.report.total_hands) * 1e6:.2f}",
            advantage=f"{(self.report.total_won / self.report.total_bet) * 100:+04.3f} %",
            timestamp = self.parameters.timestamp,
            parameters = "",#json.dumps(self.parameters.__dict__),
            rules = "",#json.dumps(Rules.__dict__),
            payload = ""#json.dumps(self.report.__dict__)
        )

        self.print_simulation_report(tbs)

        # Check if total hands exceed the threshold
        if self.report.total_hands >= DATABASE_NUMBER_OF_HANDS:
            self.insert_simulation_table(tbs)

    def print_simulation_report(self, tbs):
        # Print out the results
        self.parameters.logger.simulation("\n  -- results ---------------------------------------------------------------------\n")
        self.parameters.logger.simulation(f"    {'Number of hands':<24}: {self.report.total_hands:,}\n")
        self.parameters.logger.simulation(f"    {'Number of rounds':<24}: {self.report.total_rounds:,}\n")
        average_bet_per_hand = self.report.total_bet / self.report.total_hands
        self.parameters.logger.simulation(f"    {'Total bet':<24}: {self.report.total_bet:,} {average_bet_per_hand:+04.3f} average bet per hand\n")
        average_won_per_hand = self.report.total_won / self.report.total_hands
        self.parameters.logger.simulation(f"    {'Total won':<24}: {self.report.total_won:,} {average_won_per_hand:+04.3f} average won per hand\n")
        self.parameters.logger.simulation(f"    {'Total time':<24}: {self.report.duration:,} seconds\n")
        self.parameters.logger.simulation(f"    {'Average time':<24}: {tbs.average_time} seconds per 1,000,000 hands\n")
        self.parameters.logger.simulation(f"    {'Player advantage':<24}: {tbs.advantage}\n")
        self.parameters.logger.simulation("  --------------------------------------------------------------------------------\n\n")

    # Insert the simulation results into the database.
    def insert_simulation_table(self, simulation_table):
        url = f"http://{SIMULATION_URL}/{simulation_table.simulator}/{simulation_table.playbook}/{simulation_table.guid}"
        self.parameters.logger.simulation(f"  -- insert ----------------------------------------------------------------------\n");
        print(f"Inserting Simulation: {url}")

        try:
            # Convert the simulation table to JSON
            json_data = json.dumps(simulation_table.__dict__)
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json_data, headers=headers)

            # Handle the response
            if response.status_code != 200:
                print(f"Error inserting into Simulation table. Status: {response.status_code}")
                print(f"Response: {response.text}")
            else:
                print(f"Simulation inserted successfully. Response: {response.text}")

        except Exception as e:
            print(f"Error sending request: {e}")

        self.parameters.logger.simulation("  --------------------------------------------------------------------------------\n\n")

