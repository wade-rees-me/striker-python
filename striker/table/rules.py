import http.client
import json
from urllib.parse import urlparse
from striker.constants import RULES_URL, unescape_json, strip_quotes
from .request import Request

class Rules(Request):
    def __init__(self, decks):
        self.playbook = ""
        self.hit_soft_17 = True
        self.surrender = False
        self.double_any_two_cards = True
        self.double_after_split = False
        self.resplit_aces = False
        self.hit_split_aces = False
        self.blackjack_pays = 5
        self.blackjack_bets = 3
        self.penetration = 0.70

        try:
            url = f"http://{RULES_URL}/{decks}"
            self.fetch_json(url)
            self.fetch_table(self.json_response)
        except Exception as e:
            print(f"Error fetching rules table: {e}")
            exit(1)

    def fetch_table(self, json_data):
        try:
            # Extract rule values from the JSON
            self.playbook = json_data["playbook"]
            self.hit_soft_17 = json_data["hitSoft17"]
            self.surrender = json_data["surrender"]
            self.double_any_two_cards = json_data["doubleAnyTwoCards"]
            self.double_after_split = json_data["doubleAfterSplit"]
            self.resplit_aces = json_data["resplitAces"]
            self.hit_split_aces = json_data["hitSplitAces"]
            self.blackjack_bets = json_data["blackjackBets"]
            self.blackjack_pays = json_data["blackjackPays"]
            self.penetration = json_data["penetration"]

        except http.client.HTTPException as e:
            raise RuntimeError(f"HTTP request failed: {e}")
        except json.JSONDecodeError:
            raise RuntimeError("Error parsing JSON response")

    def print(self):
        print(f"    {'Table Rules':<24}")
        print(f"      {'Table':<24}: {self.playbook}")
        print(f"      {'Hit soft 17':<24}: {'true' if self.hit_soft_17 else 'false'}")
        print(f"      {'Surrender':<24}: {'true' if self.surrender else 'false'}")
        print(f"      {'Double any two cards':<24}: {'true' if self.double_any_two_cards else 'false'}")
        print(f"      {'Double after split':<24}: {'true' if self.double_after_split else 'false'}")
        print(f"      {'Resplit aces':<24}: {'true' if self.resplit_aces else 'false'}")
        print(f"      {'Hit split aces':<24}: {'true' if self.hit_split_aces else 'false'}")
        print(f"      {'Blackjack bets':<24}: {self.blackjack_bets}")
        print(f"      {'Blackjack pays':<24}: {self.blackjack_pays}")
        print(f"      {'Penetration':<24}: {self.penetration:.3f} %")

    def serialize(self):
        data = {
            "hit_soft_17": str(self.hit_soft_17).lower(),
            "surrender": str(self.surrender).lower(),
            "double_any_two_cards": str(self.double_any_two_cards).lower(),
            "double_after_split": str(self.double_after_split).lower(),
            "resplit_aces": str(self.resplit_aces).lower(),
            "hit_split_aces": str(self.hit_split_aces).lower(),
            "blackjack_bets": self.blackjack_bets,
            "blackjack_pays": self.blackjack_pays,
            "penetration": self.penetration
        }
        return json.dumps(data, indent=4)

