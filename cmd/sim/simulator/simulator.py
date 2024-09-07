import json
import time
from datetime import datetime, timezone
import uuid
import threading
import requests
from io import BytesIO
from sim.constants import STRIKER_WHO_AM_I, SIMULATION_URL
from sim.simulator import TableRules
from .simulation import SimulationParameters, SimulationReport, SimulationDatabaseTable
from .table import Table
from .player import Player

class SimulationManager:
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
        for table_number in range(1, parameters.tables + 1):
            table = Table(table_number, parameters)
            player = Player(parameters, table.shoe.number_of_cards)
            table.add_player(player)
            self.table_list.append(table)

        self.report = SimulationReport()

    # Run the simulation by starting sessions for all tables.
    def run_simulation(self):
        print(f"Simulation {self.name}: started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        threads = []
        for table in self.table_list:
            if self.parameters.strategy == "mimic":
                thread = threading.Thread(target=table.session_mimic)
            else:
                thread = threading.Thread(target=table.session)
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Merge the results from all tables into one report
        for table in self.table_list:
            self.report.total_rounds += table.report.total_rounds
            self.report.total_hands += table.report.total_hands
            self.report.total_bet += table.player.report.total_bet
            self.report.total_won += table.player.report.total_won
            self.report.duration += table.report.duration

        print(f"Simulation {self.name}: end at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    # Run the simulation once and process the results.
    def run_once(self):
        print("Starting striker-python simulation...")
        try:
            self.run_simulation_process()
        except Exception as e:
            print(f"Simulation failed: {e}")

    # Process the simulation and prepare a database entry for the results.
    def run_simulation_process(self):
        self.run_simulation()

        tbs = SimulationDatabaseTable(
            playbook=self.parameters.playbook,
            guid=self.parameters.guid,
            simulator=STRIKER_WHO_AM_I,
            simulations="1",
            rounds=str(self.report.total_rounds),
            hands=str(self.report.total_hands),
            total_bet=str(self.report.total_bet),
            total_won=str(self.report.total_won),
            total_time=str(int(self.report.duration)),
            average_time=f"{(self.report.duration / self.report.total_hands) * 1e6:.2f} seconds per 1,000,000 hands",
            advantage=f"{(self.report.total_won / self.report.total_bet) * 100:+04.3f} %",
            epoch = self.parameters.epoch,
            timestamp = self.parameters.timestamp,
            parameters = json.dumps(self.parameters.__dict__),
            rules = json.dumps(TableRules.__dict__),
            payload = json.dumps(self.report.__dict__)
        )

        # Insert the simulation into the database
        self.print_simulation_table(tbs)
        self.insert_simulation_table(tbs)

    def print_simulation_table(self, simulation_table):
        print()
        print(f"%-12s" % ("Report"))
        print(f"%s" % (json.dumps(simulation_table.__dict__, indent=4)))
        print()

    # Insert the simulation results into the database.
    def insert_simulation_table(self, simulation_table):
        url = f"http://{SIMULATION_URL}/{simulation_table.simulator}/{simulation_table.playbook}/{simulation_table.guid}"
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

