import sys
import threading
import multiprocessing
import os
import psutil
import time
from datetime import datetime
from striker.arguments import Arguments, Parameters, Report
from striker.table import Rules, Strategy
from striker.constants import STRIKER_WHO_AM_I
from striker.simulator import Simulator
from striker.shared import SharedValue

# import striker.xlog
from striker.xlog import init_syslog, log_info, log_error, log_fatal, close_syslog


def main():
    print(f"Start: {STRIKER_WHO_AM_I}\n")
    arguments = Arguments(sys.argv)
    parameters = Parameters(arguments)
    rules = Rules(arguments.get_decks())
    strategy = Strategy(arguments)
    finalReport = Report()

    if init_syslog():
        log_info("Simulation started at %s", datetime.now())
        log_error("Deck shuffle failed at %s", datetime.now())
        log_fatal("Fatal error: crash at %s", datetime.now())
        close_syslog()
    else:
        print("Could not initialize xlog")

    finalReport.init_report(parameters)
    print(
        f"  -- arguments -------------------------------------------------------------------"
    )
    parameters.print()
    rules.print()
    print(
        f"  --------------------------------------------------------------------------------"
    )

    processes = []
    simulators = []
    for core in range(arguments.number_of_threads.get()):
        simulator = Simulator(parameters, rules, strategy, core)
        p = multiprocessing.Process(
            target=simulator.run_simulation_process, args=(core,)
        )
        p.start()
        simulators.append(simulator)
        processes.append(p)

    for p in processes:
        p.join()

    for i, simulator in enumerate(simulators):
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
