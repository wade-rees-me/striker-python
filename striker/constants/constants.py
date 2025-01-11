import os

# General constants
STRIKER_WHO_AM_I = "striker-python"
STRIKER_VERSION = "v02.02.00"
TIME_LAYOUT = "%Y-%m-%d %H:%M:%S %z"  # Python uses strftime format, similar to Go's

# Simulation constants
MAXIMUM_NUMBER_OF_HANDS = 25000000000
MINIMUM_NUMBER_OF_HANDS = 10000
DEFAULT_NUMBER_OF_HANDS = 250000000
DATABASE_NUMBER_OF_HANDS = 250000000
MAX_SPLIT_HANDS = 18

MINIMUM_BET = 2
MAXIMUM_BET = 98
TRUE_COUNT_BET = 2
TRUE_COUNT_MULTIPLIER = 26

# Environment variables
STRATEGY_URL = os.getenv("STRIKER_URL_ACE")
STRATEGY_MLB_URL = os.getenv("STRIKER_URL_MLB")
RULES_URL = os.getenv("STRIKER_URL_RULES")
SIMULATION_URL = os.getenv("STRIKER_URL_SIMULATION")

