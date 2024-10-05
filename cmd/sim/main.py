import sys
#import argparse
import uuid
import time
from sim.arguments import Arguments, Parameters
from sim.logger import Logger
from sim.table import Rules
from sim.constants import STRATEGY_URL, STRATEGY_MLB_URL, STRIKER_WHO_AM_I, TIME_LAYOUT
from sim.simulator import Simulator

def generate_name():
    t = time.localtime()  # Get the current time
    # Format the name with the current date and time as part of the string
    name = f"{STRIKER_WHO_AM_I}_{t.tm_year:04d}_{t.tm_mon:02d}_{t.tm_mday:02d}_{int(time.time()):012d}"
    return name

def main():
    name = generate_name()
    args = Arguments()
    args.parse_arguments(sys.argv)

    logger = Logger(name, args.number_of_hands < 1000)
    rules = Rules()
    rules.rules_load_table(args.get_decks())

    params = Parameters(name, args.get_decks(), args.get_strategy(), args.get_number_of_decks(), args.number_of_hands, rules, logger)

    logger.simulation(f"Start: {STRIKER_WHO_AM_I}\n\n");
    logger.simulation(f"  -- arguments -------------------------------------------------------------------\n");
    params.print()
    rules.print(logger)
    logger.simulation(f"  --------------------------------------------------------------------------------\n\n");

    sim_manager = Simulator(params)
    sim_manager.run_simulation_process()
    logger.simulation(f"End: {STRIKER_WHO_AM_I}\n\n");

if __name__ == "__main__":
    main()

