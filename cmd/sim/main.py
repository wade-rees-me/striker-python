import argparse
import uuid
import time
from sim.arguments import CLStrategy, CLTable, CLSimulation, parse_arguments_simulation, parse_arguments_strategy, parse_arguments_table, parse_args_simulation, parse_args_strategy, parse_args_table
from sim.constants import STRATEGY_URL, STRATEGY_MLB_URL, STRIKER_WHO_AM_I, TIME_LAYOUT
from sim.simulator import SimulationParameters, SimulationManager, load_table_rules

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Striker Python Simulation")
    parse_arguments_simulation(parser)
    parse_arguments_strategy(parser)
    parse_arguments_table(parser)

    args = parser.parse_args()
    parse_args_simulation(args)
    parse_args_strategy(args)
    parse_args_table(args)

    # Set strategy URL if the Striker flag is enabled
    #if CLStrategy.machine_flag:
    #    STRATEGY_URL = STRATEGY_MLB_URL
    #    print("mlb: ", STRATEGY_MLB_URL)
    #print("url: ", STRATEGY_URL)

    # Initialize SimulationParameters
    parameters = SimulationParameters(
        guid = str(uuid.uuid4()),
        processor = STRIKER_WHO_AM_I,
        epoch = str(int(time.time())),
        timestamp = time.strftime(TIME_LAYOUT),
        decks = CLTable.get_table()[0],
        number_of_decks = CLTable.get_table()[1],
        strategy = CLStrategy.get_strategy(),
        playbook = f"{CLTable.get_table()[0]}-{CLStrategy.get_strategy()}",
        url = STRATEGY_MLB_URL if CLStrategy.machine_flag else STRATEGY_URL,
        tables = CLSimulation.tables,
        rounds = CLSimulation.rounds,
        blackjack_pays = CLSimulation.blackjack_pays,
        penetration = CLSimulation.penetration
    )

    # Load the table rules
    load_table_rules(parameters.decks)

    # Instantiate the SimulationManager class an call the run_once method on the instance
    sim_manager = SimulationManager(parameters)
    sim_manager.run_once()

if __name__ == "__main__":
    main()

