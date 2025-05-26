import multiprocessing
import sys
from striker.constants.constants import (
    NUMBER_OF_HANDS_MAXIMUM,
    NUMBER_OF_HANDS_MINIMUM,
    NUMBER_OF_HANDS_DEFAULT,
    NUMBER_OF_CORES_PHYSICAL,
    NUMBER_OF_CORES_LOGICAL,
    NUMBER_OF_CORES_DEFAULT,
    STRIKER_WHO_AM_I,
    STRIKER_VERSION,
)
from striker.shared.shared_value import SharedValue


#
class Arguments:
    def __init__(self, argv):
        self.mimic_flag = False
        self.basic_flag = False
        self.neural_flag = False
        self.linear_flag = False
        self.polynomial_flag = False
        self.high_low_flag = False
        self.wong_flag = False
        self.single_deck_flag = False
        self.double_deck_flag = False
        self.six_shoe_flag = False
        self.number_of_hands = SharedValue("i", NUMBER_OF_HANDS_DEFAULT)
        self.number_of_threads = SharedValue("i", NUMBER_OF_CORES_DEFAULT)

        i = 1  # Start from the first argument after the program name
        while i < len(argv):
            if argv[i] in ("-h", "--number-of-hands") and i + 1 < len(argv):
                self.number_of_hands.set(int(argv[i + 1]))
                if (
                    self.number_of_hands.get() < NUMBER_OF_HANDS_MINIMUM
                    or self.number_of_hands.get() > NUMBER_OF_HANDS_MAXIMUM
                ):
                    print(
                        f"Number of hands must be between {NUMBER_OF_HANDS_MINIMUM} and {NUMBER_OF_HANDS_MAXIMUM}"
                    )
                    sys.exit(1)
                i += 1  # Skip over the next argument, which is the number of hands (e.g., "10")
            elif argv[i] in ("-t", "--number-of-threads") and i + 1 < len(argv):
                self.number_of_threads.set(int(argv[i + 1]))
                if (
                    self.number_of_threads.get() < 1
                    or self.number_of_threads.get() > NUMBER_OF_CORES_LOGICAL
                ):
                    print(
                        f"Number of threads must be between {1} and {NUMBER_OF_CORES_LOGICAL}"
                    )
                    sys.exit(1)
                i += 1
            elif argv[i] in ("-M", "--mimic"):
                self.mimic_flag = True
            elif argv[i] in ("-B", "--basic"):
                self.basic_flag = True
            elif argv[i] in ("-N", "--neural"):
                self.neural_flag = True
            elif argv[i] in ("-L", "--linear"):
                self.linear_flag = True
            elif argv[i] in ("-P", "--polynomial"):
                self.polynomial_flag = True
            elif argv[i] in ("-H", "--high-low"):
                self.high_low_flag = True
            elif argv[i] in ("-W", "--wong"):
                self.wong_flag = True
            elif argv[i] in ("-1", "--single-deck"):
                self.single_deck_flag = True
            elif argv[i] in ("-2", "--double-deck"):
                self.double_deck_flag = True
            elif argv[i] in ("-6", "--six-shoe"):
                self.six_shoe_flag = True
            elif argv[i] == "--help":
                self.print_help_message()
                sys.exit(0)
            elif argv[i] == "--version":
                self.print_version()
                sys.exit(0)
            else:
                print(f"Error: Invalid argument: {argv[i]}")
                sys.exit(2)
            i += 1  # Move to the next argument

    def print_version(self):
        print(f"{STRIKER_WHO_AM_I}: version: {STRIKER_VERSION}")

    def print_help_message(self):
        print("Usage: strikerPython [options]")
        print("Options:")
        print("  --help                                    Show this help message")
        print("  --version                                 Display the program version")
        print(
            "  -h, --number-of-hands <number of hands>     The number of hands to play in this simulation"
        )
        print(
            "  -t, --number-of-threads <number of threads> The number of hands to play in this simulation"
        )
        print(
            "  -M, --mimic                                 Use the mimic dealer player strategy"
        )
        print(
            "  -B, --basic                                 Use the basic player strategy"
        )
        print(
            "  -N, --neural                                Use the neural player strategy"
        )
        print(
            "  -L, --linear                                Use the linear regression player strategy"
        )
        print(
            "  -P, --polynomial                            Use the polynomial regression player strategy"
        )
        print(
            "  -H, --high-low                              Use the high-low count player strategy"
        )
        print(
            "  -W, --wong                                  Use the Wong count player strategy"
        )
        print(
            "  -1, --single-deck                           Use a single deck of cards and rules"
        )
        print(
            "  -2, --double-deck                           Use a double deck of cards and rules"
        )
        print(
            "  -6, --six-shoe                              Use a six-deck shoe of cards and rules"
        )

    def get_strategy(self):
        if self.mimic_flag:
            return "mimic"
        if self.polynomial_flag:
            return "polynomial"
        if self.linear_flag:
            return "linear"
        if self.neural_flag:
            return "neural"
        if self.high_low_flag:
            return "high-low"
        if self.wong_flag:
            return "wong"
        return "basic"

    def get_decks(self):
        if self.double_deck_flag:
            return "double-deck"
        if self.six_shoe_flag:
            return "six-shoe"
        return "single-deck"

    def get_number_of_decks(self):
        if self.double_deck_flag:
            return 2
        if self.six_shoe_flag:
            return 6
        return 1
