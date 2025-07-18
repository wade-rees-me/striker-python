import os
import json
import socket
import requests


# General constants
STRIKER_WHO_AM_I = "striker-python"
STRIKER_VERSION = "v3.00.00"
TIME_LAYOUT = "%Y-%m-%d %H:%M:%S %z"  # Python uses strftime format, similar to Go's
MY_HOSTNAME = "Striker"

#
NUMBER_OF_CARDS_IN_DECK = 52
NUMBER_OF_CORES_PHYSICAL = 24
NUMBER_OF_CORES_LOGICAL = 32
NUMBER_OF_CORES_DEFAULT = 24

# Define the maximum size string fields
MAX_STRING_SIZE = 512
MAX_BUFFER_SIZE = 8192
MAX_MEMORY_SIZE = 536870912

# Simulation constants
MILLION = 1000000
BILLION = MILLION * 1000
NUMBER_OF_HANDS_MAXIMUM = BILLION * 10
NUMBER_OF_HANDS_MINIMUM = 1000
NUMBER_OF_HANDS_DEFAULT = MILLION * 100
NUMBER_OF_HANDS_DATABASE = MILLION * 100

# Simulation constants
MAX_SPLIT_HANDS = 18
STATUS_ROUNDS = 10000

MINIMUM_BET = 2
MAXIMUM_BET = 20
TRUE_COUNT_BET = 2
TRUE_COUNT_MULTIPLIER = 26

# Environment variables
RULES_URL = os.getenv("STRIKER_URL_RULES")
CHARTS_URL = os.getenv("STRIKER_URL_CHARTS")
SIMULATIONS_URL = os.getenv("STRIKER_URL_SIMULATIONS")


def is_my_computer():
    try:
        hostname = socket.gethostname()
        my_hostname = MY_HOSTNAME
        return hostname == my_hostname
    except Exception as e:
        print(f"Error getting hostname: {e}")
        return False


# def read_json_file(filename):
#    try:
#        with open(filename, "r") as file:
#            return file.read()
#    except FileNotFoundError:
#        print(f"Error: File not found - {filename}")
#        return None
#    except OSError as e:
#        print(f"Error opening file: {filename} - {e}")
#        return None


def unescape_json(s: str) -> str:
    """Unescapes JSON-style escape sequences in a string."""
    return s.encode().decode("unicode_escape")


def strip_quotes(s: str) -> str:
    """Removes surrounding double quotes from a string."""
    if len(s) > 1 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s
