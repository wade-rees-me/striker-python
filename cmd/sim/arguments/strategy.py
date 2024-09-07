import argparse

class CLStrategyStruct:
    def __init__(self):
        """
        Initializes a new CLStrategyStruct object with default strategy flags set to False.
        """
        self.mimic_flag = False
        self.basic_flag = False
        self.linear_flag = False
        self.polynomial_flag = False
        self.high_low_flag = False
        self.wong_flag = False
        self.machine_flag = False

    def get_strategy(self):
        """
        Returns the chosen strategy based on the flags set.
        """
        if self.mimic_flag:
            return "mimic"
        if self.polynomial_flag:
            return "polynomial"
        if self.linear_flag:
            return "linear"
        if self.high_low_flag:
            return "high-low"
        if self.wong_flag:
            return "wong"
        if self.machine_flag:
            return "machine"
        return "basic"

# Create an instance of CLStrategyStruct
CLStrategy = CLStrategyStruct()

# Define command-line flags for strategies
def parse_arguments_strategy(parser):
    parser.add_argument(
        '--strategy-mimic',
        action='store_true',
        help="Use the mimic the dealer strategy tables."
    )
    
    parser.add_argument(
        '--strategy-basic',
        action='store_true',
        help="Use the basic strategy tables (default)."
    )
    
    parser.add_argument(
        '--strategy-linear',
        action='store_true',
        help="Use the linear regression strategy tables."
    )
    
    parser.add_argument(
        '--strategy-polynomial',
        action='store_true',
        help="Use the polynomial regression strategy tables."
    )
    
    parser.add_argument(
        '--strategy-high-low',
        action='store_true',
        help="Use the High Low strategy tables."
    )
    
    parser.add_argument(
        '--strategy-wong',
        action='store_true',
        help="Use the Wong strategy tables."
    )
    
    parser.add_argument(
        '--strategy-machine',
        action='store_true',
        help="Use the Striker strategy tables."
    )

# Parse arguments and assign them to the CLStrategy object
def parse_args_strategy(args):
    CLStrategy.mimic_flag = args.strategy_mimic
    CLStrategy.basic_flag = args.strategy_basic
    CLStrategy.linear_flag = args.strategy_linear
    CLStrategy.polynomial_flag = args.strategy_polynomial
    CLStrategy.high_low_flag = args.strategy_high_low
    CLStrategy.wong_flag = args.strategy_wong
    CLStrategy.machine_flag = args.strategy_machine

