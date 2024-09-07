import argparse

class CLTableStruct:
    def __init__(self):
        """
        Initializes the CLTableStruct object with default table flags set to False.
        """
        self.deck_single_flag = False
        self.deck_double_flag = False
        self.deck_multi_flag = False

    def get_table(self):
        """
        Returns the table type and the number of decks based on the flags set.
        :return: A tuple containing the table type as a string and the number of decks as an integer.
        """
        if self.deck_double_flag:
            return "double-deck", 2
        if self.deck_multi_flag:
            return "six-shoe", 6
        return "single-deck", 1

# Create an instance of CLTableStruct
CLTable = CLTableStruct()

# Define command-line flags for table configurations
def parse_arguments_table(parser):
    parser.add_argument(
        '--table-single-deck',
        action='store_true',
        help="Use a single deck table (default)."
    )
    
    parser.add_argument(
        '--table-double-deck',
        action='store_true',
        help="Use a double deck table."
    )
    
    parser.add_argument(
        '--table-six-shoe',
        action='store_true',
        help="Use a six shoe table (6 deck shoe)."
    )

# Parse the arguments and assign them to the CLTable object
def parse_args_table(args):
    CLTable.deck_single_flag = args.table_single_deck
    CLTable.deck_double_flag = args.table_double_deck
    CLTable.deck_multi_flag = args.table_six_shoe

