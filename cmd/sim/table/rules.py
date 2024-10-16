import requests
import json
from sim.constants import RULES_URL

#
class Rules:
    def __init__(self):
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

    def rules_load_table(self, decks):
        try:
            url = f"http://{RULES_URL}/{decks}"
            self.rules_fetch_table(url)
        except Exception as e:
            print(f"Error fetching rules table: {e}")
            exit(1)

    def rules_fetch_table(self, url):
        try:
            # Use requests to fetch the data
            response = requests.get(url)
            response.raise_for_status()

            # Parse the JSON data
            json_data = response.json()
            payload = json_data.get("payload")
            json_payload = json.loads(payload)

            # Extract rule values from the JSON
            self.playbook = json_payload["playbook"]
            self.hit_soft_17 = json_payload["hitSoft17"]
            self.surrender = json_payload["surrender"]
            self.double_any_two_cards = json_payload["doubleAnyTwoCards"]
            self.double_after_split = json_payload["doubleAfterSplit"]
            self.resplit_aces = json_payload["resplitAces"]
            self.hit_split_aces = json_payload["hitSplitAces"]
            self.blackjack_bets = json_payload["blackjackBets"]
            self.blackjack_pays = json_payload["blackjackPays"]
            self.penetration = json_payload["penetration"]
        
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching rules table: {e}")
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

