import sys
from striker.arguments import Arguments, Parameters
from striker.table import Rules, Strategy
from striker.constants import STRIKER_WHO_AM_I
from striker.simulator import Simulator

def main():
    print(f"Start: {STRIKER_WHO_AM_I}\n")
    arguments = Arguments(sys.argv)
    parameters = Parameters(arguments.get_decks(), arguments.get_strategy(), arguments.get_number_of_decks(), arguments.number_of_hands)
    rules = Rules(arguments.get_decks())
    strategy = Strategy(arguments.get_decks(), arguments.get_strategy(), arguments.get_number_of_decks() * 52)
    simulator = Simulator(parameters, rules, strategy)

    print(f"  -- arguments -------------------------------------------------------------------")
    parameters.print()
    rules.print()
    print(f"  --------------------------------------------------------------------------------\n")

    simulator.run_simulation_process()
    print(f"End: {STRIKER_WHO_AM_I}\n")

if __name__ == "__main__":
    main()

