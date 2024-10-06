import requests
import json
import sys

from sim.cards import Card
from sim.constants import STRATEGY_URL

BET = "bet"
INSURANCE = "insurance"
SURRENDER = "surrender"
DOUBLE = "double"
SPLIT = "split"
STAND = "stand"
PLAY = "play"

class Strategy:
    def __init__(self, playbook, number_of_cards):
        self.playbook = playbook
        self.number_of_cards = number_of_cards
        self.json_object = None
        self.urlBet = f"http://{STRATEGY_URL}/{BET}"
        self.urlInsurance = f"http://{STRATEGY_URL}/{INSURANCE}"
        self.urlSurrender = f"http://{STRATEGY_URL}/{SURRENDER}"
        self.urlDouble = f"http://{STRATEGY_URL}/{DOUBLE}"
        self.urlSplit = f"http://{STRATEGY_URL}/{SPLIT}"
        self.urlStand = f"http://{STRATEGY_URL}/{STAND}"
        self.urlPlay = f"http://{STRATEGY_URL}/{PLAY}"

        # Create a session object
        self.session = requests.Session()

        # Close the session when done
        #self.session.close()

    def get_strategy_url(self):
        return STRATEGY_URL

    def get_bet(self, seen_cards):
        self.json_object = None
        return self.parse_aux_int(self.http_get(self.urlBet, self.build_params(seen_cards, None, None, None)), BET, 2)

    def get_insurance(self, seen_cards):
        return self.parse_aux_bool(self.http_get(self.urlInsurance, self.build_params(seen_cards, None, None, None)), INSURANCE, False)

    def get_surrender(self, seen_cards, have_cards, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, SURRENDER, False)
        return self.parse_aux_bool(self.http_get(self.urlSurrender, self.build_params(seen_cards, have_cards, None, up)), SURRENDER, False)

    def get_double(self, seen_cards, have_cards, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, DOUBLE, False)
        return self.parse_aux_bool(self.http_get(self.urlDouble, self.build_params(seen_cards, have_cards, None, up)), DOUBLE, False)

    def get_split(self, seen_cards, pair: Card, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, SPLIT, False)
        return self.parse_aux_bool(self.http_get(self.urlSplit, self.build_params(seen_cards, None, pair, up)), SPLIT, False)

    def get_stand(self, seen_cards, have_cards, up: Card):
        if self.json_object:
            return self.parse_aux_bool(self.json_object, STAND, True)
        return self.parse_aux_bool(self.http_get(self.urlStand, self.build_params(seen_cards, have_cards, None, up)), STAND, True)

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
            response = self.session.get(url, params=params)
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

