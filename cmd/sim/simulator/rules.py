import requests
import json
from sim.constants import RULES_URL

class RulesTableStruct:
    """
    Represents the rules table structure, with attributes corresponding to the
    fields in the JSON response.
    """
    def __init__(self, playbook="", hit_soft_17=False, surrender=False, double_any_two_cards=False,
                 double_after_split=False, resplit_aces=False, hit_split_aces=False, blackjack_pays="",
                 penetration=0.0):
        self.playbook = playbook
        self.hit_soft_17 = hit_soft_17
        self.surrender = surrender
        self.double_any_two_cards = double_any_two_cards
        self.double_after_split = double_after_split
        self.resplit_aces = resplit_aces
        self.hit_split_aces = hit_split_aces

# Global variable to hold the table rules
TableRules = RulesTableStruct()

def load_table_rules(decks):
    """
    Load table rules by fetching the JSON data from the server.
    :param decks: The deck type (e.g., "single", "double", etc.)
    """
    url = f"http://{RULES_URL}/{decks}"
    if not fetch_rules_table(url):
        raise Exception("Failed to load table rules")

def fetch_rules_table(url):
    """
    Fetches the rules table from the given URL and updates the global TableRules object.
    :param url: The URL to fetch the rules from.
    :return: True if successful, False otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        # Update the TableRules object with the fetched data
        global TableRules
        TableRules = RulesTableStruct(
            playbook=data.get("playbook", ""),
            hit_soft_17=data.get("hitSoft17", False),
            surrender=data.get("surrender", False),
            double_any_two_cards=data.get("doubleAnyTwoCards", False),
            double_after_split=data.get("doubleAfterSplit", False),
            resplit_aces=data.get("resplitAces", False),
            hit_split_aces=data.get("hitSplitAces", False),
            blackjack_pays=data.get("blackjackPays", ""),
            penetration=data.get("penetration", 0.0)
        )
        return True
    except (requests.RequestException, ValueError) as err:
        print(f"Error fetching rules table: {err}")
        return False

