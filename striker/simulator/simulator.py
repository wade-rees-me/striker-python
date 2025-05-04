import json
import http.client
import time
from datetime import datetime, timezone
import uuid
from io import BytesIO
from urllib.parse import urlparse
from striker.arguments import Parameters, Report
from striker.constants import (
    STRIKER_WHO_AM_I,
    SIMULATIONS_URL,
)
from striker.table import Rules
from .table import Table
from .player import Player


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
        self.table = Table(1, parameters, rules)
        self.report = Report()

        player = Player(parameters, rules, strategy, self.table.shoe.number_of_cards)
        self.table.add_player(player)

    # Run the simulation by starting sessions for all tables.
    def run_simulation(self):
        self.table.session(self.parameters.strategy == "mimic")
        self.report.merge_report(self.table.player.report)
        self.report.total_rounds += self.table.report.total_rounds
        self.report.total_hands += self.table.report.total_hands

    # Process the simulation and prepare a database entry for the results.
    def run_simulation_process(self):
        self.run_simulation()
