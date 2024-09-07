import requests
import json
from urllib.parse import urlencode, urljoin
from sim.constants import MINIMUM_BET, MAXIMUM_BET, STRATEGY_URL
from .simulation import SimulationParameters


class AuxResponse:
    def __init__(self, bet=0, insurance=False, double=False, split=False, surrender=False, stand=True):
        self.bet = bet
        self.insurance = insurance
        self.double = double
        self.split = split
        self.surrender = surrender
        self.stand = stand


class PlayerStrategy:
    def __init__(self, parameters, number_of_cards):
        """
        Initialize a Player instance.
        :param parameters: SimulationParameters object
        :param number_of_cards: Total number of cards in the game
        """
        self.seen_cards = [0] * 13  # Similar to SeenCards array in Go
        self.parameters = parameters
        self.number_of_cards = number_of_cards

    def get_bet(self, seen_cards):
        """
        Get the player's bet by making a request to the 'bet' endpoint.
        :return: The bet amount, clamped between MINIMUM_BET and MAXIMUM_BET.
        """
        try:
            url = build_url("bet", seen_cards, None, 0, self.parameters.playbook, self.number_of_cards, 0, self.parameters.url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return clamp_int(aux['bet'], MINIMUM_BET, MAXIMUM_BET)
        except Exception as e:
            raise Exception(f"Failed to get bet: {e}")

    def get_insurance(self, seen_cards):
        """
        Get whether insurance is available by making a request to the 'insurance' endpoint.
        :return: True if insurance is recommended, False otherwise.
        """
        try:
            url = build_url("insurance", seen_cards, None, 0, self.parameters.playbook, self.number_of_cards, 0, self.parameters.url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return aux['insurance']
        except Exception as e:
            #print(e)
            return False

    def get_surrender(self, have, up, seen_cards):
        """
        Check if surrender is recommended by making a request to the 'surrender' endpoint.
        :param have: Cards the player has
        :param up: Dealer's up card
        :return: True if surrender is recommended, False otherwise.
        """
        try:
            url = build_url("surrender", seen_cards, have, 0, self.parameters.playbook, self.number_of_cards, up, self.parameters.url)
            #print(url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return aux['surrender']
        except Exception as e:
            print(e)
            return False

    def get_double(self, have, up, seen_cards):
        """
        Check if doubling down is recommended by making a request to the 'double' endpoint.
        :param have: Cards the player has
        :param up: Dealer's up card
        :return: True if doubling is recommended, False otherwise.
        """
        try:
            url = build_url("double", seen_cards, have, 0, self.parameters.playbook, self.number_of_cards, up, self.parameters.url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return aux['double']
        except Exception as e:
            print(e)
            return False

    def get_split(self, pair, up, seen_cards):
        """
        Check if splitting is recommended by making a request to the 'split' endpoint.
        :param pair: Pair value of the player's cards
        :param up: Dealer's up card
        :return: True if splitting is recommended, False otherwise.
        """
        try:
            url = build_url("split", seen_cards, None, pair, self.parameters.playbook, self.number_of_cards, up, self.parameters.url)
            #print(url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return aux['split']
        except Exception as e:
            print(e)
            return False

    def get_stand(self, have, up, seen_cards):
        """
        Check if standing is recommended by making a request to the 'stand' endpoint.
        :param have: Cards the player has
        :param up: Dealer's up card
        :return: True if standing is recommended, False otherwise.
        """
        try:
            url = build_url("stand", seen_cards, have, 0, self.parameters.playbook, self.number_of_cards, up, self.parameters.url)
            response = requests.get(url)
            response.raise_for_status()
            aux = response.json()
            return aux['stand']
        except Exception as e:
            print(e)
            return True


def build_url(endpoint, seen_data, have_data, pair, playbook, cards, up, url):
    """
    Build a URL for the API request.
    :param endpoint: The API endpoint to call.
    :param seen_data: Cards seen so far.
    :param have_data: Cards in hand.
    :param pair: Pair value for split check.
    :param playbook: The playbook to use.
    :param cards: Total number of cards.
    :param up: Dealer's up card.
    :return: The full URL with query parameters.
    """
    #base_url = f"http://{STRATEGY_URL}/{endpoint}"
    base_url = f"http://{url}/{endpoint}"
    params = {
        'playbook': playbook,
        'cards': cards,
        'up': up,
        'pair': pair
    }
    
    if seen_data:
        params['seen'] = json.dumps(seen_data)
    
    if have_data:
        params['have'] = json.dumps(have_data)
    
    return f"{base_url}?{urlencode(params)}"


def clamp_int(value, min_value, max_value):
    """
    Clamp the integer value between min_value and max_value.
    :param value: The value to clamp.
    :param min_value: The minimum allowed value.
    :param max_value: The maximum allowed value.
    :return: The clamped value.
    """
    return max(min_value, min(value, max_value))

