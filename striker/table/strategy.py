import http.client
import json
from urllib.parse import urlparse
from striker.constants import TRUE_COUNT_BET, TRUE_COUNT_MULTIPLIER, CHARTS_URL, unescape_json, strip_quotes
from striker.cards import Card
from .chart import Chart
from .request import Request

MAX_VALUES = 13
#MAX_ENTRIES = 22
#MAX_STRING_SIZE = 8

class Strategy(Request):
    def __init__(self, decks, playbook, number_of_cards):
        self.request = {}
        self.Playbook = ""
        self.Counts = [0] * MAX_VALUES
        self.Insurance = ""

        self.SoftDouble = Chart("Soft Double")
        self.HardDouble = Chart("Hard Double")
        self.PairSplit = Chart("Pair Split")
        self.SoftStand = Chart("Soft Stand")
        self.HardStand = Chart("Hard Stand")

        self.number_of_cards = number_of_cards

        if playbook.lower() != "mimic":
            url = f"http://{CHARTS_URL}/{decks}/{playbook}"
            self.fetch_json(url)
            self.fetch_table(self.json_response)

            self.SoftDouble.chart_print()
            self.HardDouble.chart_print()
            self.PairSplit.chart_print()
            self.SoftStand.chart_print()
            self.HardStand.chart_print()
            self.count_print()

    def fetch_table(self, payload):
        self.Playbook = payload.get("playbook", "")
        self.Insurance = payload.get("insurance", "")
        self.Counts = payload.get("counts", [0] * MAX_VALUES)
        self.Counts.insert(0, 0)
        self.Counts.insert(0, 0)
        self.load_table(payload.get("soft-double"), self.SoftDouble)
        self.load_table(payload.get("hard-double"), self.HardDouble)
        self.load_table(payload.get("pair-split"), self.PairSplit)
        self.load_table(payload.get("soft-stand"), self.SoftStand)
        self.load_table(payload.get("hard-stand"), self.HardStand)

    def load_table(self, data, chart):
        if data is not None:
            for key, values in data.items():
                for i, value in enumerate(values):
                    chart.chart_insert(key, 2 + i, value)

    def get_bet(self, seen_cards):
        return self.get_true_count(seen_cards, self.get_running_count(seen_cards)) * TRUE_COUNT_BET

    def get_insurance(self, seen_cards):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        return self.process_value(self.Insurance, true_count, False)

    def get_double(self, seen_cards, total, soft, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        if soft:
            return self.process_value(self.SoftDouble.chart_get_value(str(total), up.value), true_count, False)
        return self.process_value(self.HardDouble.chart_get_value(str(total), up.value), true_count, False)

    def get_split(self, seen_cards, pair: Card, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        return self.process_value(self.PairSplit.chart_get_value(pair.key, up.value), true_count, False)

    def get_stand(self, seen_cards, total, soft, up: Card):
        true_count = self.get_true_count(seen_cards, self.get_running_count(seen_cards))
        if soft:
            return self.process_value(self.SoftStand.chart_get_value(str(total), up.value), true_count, False)
        return self.process_value(self.HardStand.chart_get_value(str(total), up.value), true_count, False)

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

    def count_print(self):
        print("Counts")
        print("--------------------2-----3-----4-----5-----6-----7-----8-----9-----X-----A---")
        print(f"   :", end=" ")
        print(" ".join(f"{count:4}," for count in self.Counts))
        print("------------------------------------------------------------------------------\n")

