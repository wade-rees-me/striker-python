import sys
from striker.arguments import Arguments, Parameters, Report
from striker.table import Rules, Strategy
from striker.constants import STRIKER_WHO_AM_I
from striker.simulator import Simulator


def main():
    print(f"Start: {STRIKER_WHO_AM_I}\n")
    arguments = Arguments(sys.argv)
    parameters = Parameters(
        arguments.get_decks(),
        arguments.get_strategy(),
        arguments.get_number_of_decks(),
        arguments.number_of_hands,
    )
    rules = Rules(arguments.get_decks())
    strategy = Strategy(
        arguments.get_decks(),
        arguments.get_strategy(),
        arguments.get_number_of_decks() * 52,
    )
    simulator = Simulator(parameters, rules, strategy)
    finalReport = Report()

    finalReport.init_report(parameters)
    print(
        f"  -- arguments -------------------------------------------------------------------"
    )
    parameters.print()
    rules.print()
    print(
        f"  --------------------------------------------------------------------------------"
    )

    simulator.run_simulation_process()
    finalReport.merge_report(simulator.report)
    finalReport.finish_report()

    print(
        f"  -- results ---------------------------------------------------------------------"
    )
    finalReport.print_report()
    print(
        f"  --------------------------------------------------------------------------------"
    )
    print(
        f"  -- insert  ---------------------------------------------------------------------"
    )
    finalReport.insert_report()
    print(
        f"  --------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    main()
