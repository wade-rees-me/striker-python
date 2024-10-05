import requests
import json
import sys

from sim.cards import Card
from sim.constants import STRATEGY_URL

class Strategy:
    def __init__(self, playbook, number_of_cards):
        self.playbook = playbook
        self.number_of_cards = number_of_cards
        self.json_object = None
        self.urlBet = f"http://{STRATEGY_URL}/bet"
        self.urlInsurance = f"http://{STRATEGY_URL}/insurance"
        self.urlSurrender = f"http://{STRATEGY_URL}/surrender"
        self.urlDouble = f"http://{STRATEGY_URL}/double"
        self.urlSplit = f"http://{STRATEGY_URL}/split"
        self.urlStand = f"http://{STRATEGY_URL}/stand"
        self.urlPlay = f"http://{STRATEGY_URL}/play"

    def get_strategy_url(self):
        return STRATEGY_URL

    def get_bet(self, seen_cards):
        self.json_object = None
        return self.parse_aux_int(self.http_get(self.urlBet, self.build_params(seen_cards, None, None, None)), "bet", 2)

    def get_insurance(self, seen_cards):
        #return self.parse_aux_bool(self.http_get(self.urlInsurance, self.build_params(seen_cards, None, None, None)), "insurance", False)
        #print(f"insurance")
        return False

    def get_surrender(self, seen_cards, have_cards):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, "surrender", False)
        return self.parse_aux_bool(self.http_get(self.urlSurrender, self.build_params(seen_cards, have_cards, None, None)), "surrender", False)

    def get_double(self, seen_cards, have_cards, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, "double", False)
        return self.parse_aux_bool(self.http_get(self.urlDouble, self.build_params(seen_cards, have_cards, None, up)), "double", False)

    def get_split(self, seen_cards, pair: Card, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, "split", False)
        return self.parse_aux_bool(self.http_get(self.urlSplit, self.build_params(seen_cards, None, pair, up)), "split", False)

    def get_stand(self, seen_cards, have_cards, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, "stand", True)
        #print(f"stand {self.parse_aux_bool(self.http_get(self.urlStand, self.build_params(seen_cards, have_cards, None, up)), "stand", True)}")
        return self.parse_aux_bool(self.http_get(self.urlStand, self.build_params(seen_cards, have_cards, None, up)), "stand", True)

    def do_play(self, seen_cards, have_cards, pair: Card, up: Card):
        self.json_object = self.http_get(self.urlPlay, self.build_params(seen_cards, have_cards, pair, up))

    def clear(self):
        self.json_object = None

    def build_params(self, seen_data, have_data, pair: Card, up: Card):
        params = {
            "playbook": self.playbook,
            "cards": str(self.number_of_cards)
        }
        if up:
            params["up"] = str(up.get_offset())
        if pair:
            params["pair"] = str(pair.get_value())
        if seen_data:
            params["seen"] = json.dumps(seen_data)
        if have_data:
            params["have"] = json.dumps(have_data)
        return params

    def http_get(self, url, params):
        #print(f"url: {url}/{params}")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Failed to parse JSON")
            sys.exit(1)

    def parse_aux_int(self, json_data, key, default):
        return int(json_data.get(key, default))

    def parse_aux_bool(self, json_data, key, default):
        return bool(json_data.get(key, default))

