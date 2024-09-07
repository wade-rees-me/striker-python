import os

# General constants
STRIKER_VERSION = "v01.00.01"
TIME_LAYOUT = "%Y-%m-%d %H:%M:%S %z"  # Python uses strftime format, similar to Go's

# Simulation constants
MAX_NUMBER_OF_ROUNDS = 1000000000
MIN_NUMBER_OF_ROUNDS = 10000
DEFAULT_NUMBER_OF_ROUNDS = 1000000
MAX_NUMBER_OF_TABLES = 4
MIN_NUMBER_OF_TABLES = 1
MAX_SPLIT_HANDS = 3
STRIKER_WHO_AM_I = "striker-python"

MINIMUM_BET = 2
MAXIMUM_BET = 98

# Environment variables
STRATEGY_URL = os.getenv("STRIKER_URL_ACE")
STRATEGY_MLB_URL = os.getenv("STRIKER_URL_MLB")
RULES_URL = os.getenv("STRIKER_URL_RULES")
SIMULATION_URL = os.getenv("STRIKER_URL_SIMULATION")

