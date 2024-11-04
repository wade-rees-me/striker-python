import json
import requests
from sim.constants import TRUE_COUNT_BET, TRUE_COUNT_MULTIPLIER
from sim.cards import Card

MAX_VALUES = 13
MAX_ENTRIES = 22
MAX_STRING_SIZE = 8

class Strategy:
    def __init__(self, decks, playbook, number_of_cards):
        self.request = {}
        self.Playbook = ""
        self.Counts = [0] * MAX_VALUES
        self.Bets = [0] * MAX_VALUES
        self.Insurance = ""
        self.SoftDouble = [[" " * MAX_STRING_SIZE for _ in range(MAX_VALUES)] for _ in range(MAX_ENTRIES)]
        self.HardDouble = [[" " * MAX_STRING_SIZE for _ in range(MAX_VALUES)] for _ in range(MAX_ENTRIES)]
        self.PairSplit = [[" " * MAX_STRING_SIZE for _ in range(MAX_VALUES)] for _ in range(MAX_ENTRIES)]
        self.SoftStand = [[" " * MAX_STRING_SIZE for _ in range(MAX_VALUES)] for _ in range(MAX_ENTRIES)]
        self.HardStand = [[" " * MAX_STRING_SIZE for _ in range(MAX_VALUES)] for _ in range(MAX_ENTRIES)]
        self.number_of_cards = number_of_cards

        if playbook.lower() != "mimic":
            self.fetch_json("http://localhost:57910/striker/v1/strategy")
            self.fetch_table(decks, playbook)

    def fetch_json(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.request['jsonResponse'] = response.json()
        except requests.RequestException as e:
            print(f"Error fetching JSON: {e}")
            exit(1)

    def fetch_table(self, decks, playbook):
        for item in self.request['jsonResponse']:
            if item.get("playbook") == decks and item.get("hand") == playbook:
                payload = json.loads(item.get("payload"))
                self.Playbook = payload.get("playbook", "")
                self.Counts = payload.get("counts", [0] * MAX_VALUES)
                self.Bets = payload.get("bets", [0] * MAX_VALUES)
                self.Insurance = payload.get("insurance", "")
                self.load_table(payload.get("soft-double"), self.SoftDouble)
                self.load_table(payload.get("hard-double"), self.HardDouble)
                self.load_table(payload.get("pair-split"), self.PairSplit)
                self.load_table(payload.get("soft-stand"), self.SoftStand)
                self.load_table(payload.get("hard-stand"), self.HardStand)
                break

    def load_table(self, data, table):
        if data is not None:
            for key, values in data.items():
                entry = int(key)
                for i, value in enumerate(values):
                    table[entry][i] = value

    def get_bet(self, seen_cards):
        return self.get_true_count(seen_cards, self.get_running_count(seen_cards)) * TRUE_COUNT_BET

    def get_insurance(self, seen_cards):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        return self.process_value(self.Insurance, true_count, False);

    def get_double(self, seen_cards, total, soft, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        if soft:
            return self.process_value(self.SoftDouble[total][up.offset], true_count, False);
        return self.process_value(self.HardDouble[total][up.offset], true_count, False);

    def get_split(self, seen_cards, pair: Card, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        return self.process_value(self.PairSplit[pair.value][up.offset], true_count, False);

    def get_stand(self, seen_cards, total, soft, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        if soft:
            return self.process_value(self.SoftStand[total][up.offset], true_count, False);
        return self.process_value(self.HardStand[total][up.offset], true_count, False);

    def get_running_count(self, seen_cards):
        return sum(c * s for c, s in zip(self.Counts, seen_cards))

    def get_true_count(self, seen_cards, running_count):
        unseen = self.number_of_cards - sum(seen_cards[2:12])
        if unseen > 0:
            return int(float(running_count) / (float(unseen) / float(TRUE_COUNT_MULTIPLIER)))
        return 0

    def process_value(self, value, true_count, missing_value):
        if not value:
            return missing_value
        if value.lower() in ["yes", "y"]:
            return True
        elif value.lower() in ["no", "n"]:
            return False
        elif value[0].lower() == "r":
            return true_count <= int(value[1:])
        return true_count >= int(value)
    
