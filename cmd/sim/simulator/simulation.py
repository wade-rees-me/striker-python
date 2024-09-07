import json
import time
import uuid
import requests
from io import BytesIO

# Initialize the simulation report to track metrics.
class SimulationReport:
    def __init__(self):
        self.total_rounds = 0
        self.total_hands = 0
        self.total_bet = 0
        self.total_won = 0
        self.start = time.time()
        self.end = 0
        self.duration = 0

# Initialize a SimulationDatabaseTable for storing results.
class SimulationDatabaseTable:
    def __init__(self, playbook, guid, simulator, simulations, rounds, hands, total_bet, total_won, total_time, average_time, advantage, epoch, timestamp, parameters, rules, payload):
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
        self.epoch = epoch
        self.timestamp = timestamp
        self.parameters = parameters
        self.rules = rules
        self.payload = payload

# Initialize a SimulationParameters object
class SimulationParameters:
    def __init__(self, guid, processor, epoch, timestamp, decks, strategy, playbook, blackjack_pays, tables, rounds, number_of_decks, penetration, url):
        self.guid = guid
        self.processor = processor
        self.epoch = epoch
        self.timestamp = timestamp
        self.decks = decks
        self.strategy = strategy
        self.playbook = playbook
        self.blackjack_pays = blackjack_pays
        self.tables = tables
        self.rounds = rounds
        self.number_of_decks = number_of_decks
        self.penetration = penetration
        self.url = url

