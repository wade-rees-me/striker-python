import argparse
from sim.constants.constants import MAX_NUMBER_OF_TABLES, MIN_NUMBER_OF_TABLES, MAX_NUMBER_OF_ROUNDS, MIN_NUMBER_OF_ROUNDS

class CLSimulationStruct:
    def __init__(self):
        self.tables = MIN_NUMBER_OF_TABLES
        self.rounds = MIN_NUMBER_OF_ROUNDS
        self.blackjack_pays = "3:2"
        self.penetration = 0.75

# Create an instance of the simulation class
CLSimulation = CLSimulationStruct()

# Define command-line arguments with argparse
def parse_arguments_simulation(parser):
    parser.add_argument(
        '--number-of-tables',
        type=int,
        default=MIN_NUMBER_OF_TABLES,
        help=f'Number of tables (minimum {MIN_NUMBER_OF_TABLES}; maximum {MAX_NUMBER_OF_TABLES}).'
    )
    
    parser.add_argument(
        '--number-of-rounds',
        type=int,
        default=MIN_NUMBER_OF_ROUNDS,
        help=f'Number of rounds (minimum {MIN_NUMBER_OF_ROUNDS}; maximum {MAX_NUMBER_OF_ROUNDS}).'
    )
    
    parser.add_argument(
        '--table-blackjack-pays',
        type=str,
        default="3:2",
        help="Set the payout for blackjack pays (default is 3:2)."
    )
    
    parser.add_argument(
        '--table-penetration',
        type=float,
        default=0.75,
        help="Set the deck penetration before shuffle (default is 0.75)."
    )

# Parse the arguments and update the CLSimulation object
def parse_args_simulation(args):
    CLSimulation.tables = args.number_of_tables
    CLSimulation.rounds = args.number_of_rounds
    CLSimulation.blackjack_pays = args.table_blackjack_pays
    CLSimulation.penetration = args.table_penetration

