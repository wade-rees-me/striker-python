import os
import threading
import datetime

class Logger:
    def __init__(self, name, debug_flag):
        self.name = name
        self.debug_flag = debug_flag
        self.log_mutex = threading.Lock()

        # Define directory and subdirectory
        self.directory = self.get_simulation_directory()
        self.subdirectory = self.get_subdirectory()

        # Ensure directories exist
        full_path = os.path.join(self.directory, self.subdirectory)
        os.makedirs(full_path, exist_ok=True)

        # File names for simulation and debug logs
        self.simulation_file_name = os.path.join(full_path, f"{name}_simulation.txt")
        self.simulation_file = open(self.simulation_file_name, 'w')

        if self.debug_flag:
            self.debug_file_name = os.path.join(full_path, f"{name}_debug.txt")
            self.debug_file = open(self.debug_file_name, 'w')
        else:
            self.debug_file = None

    def __del__(self):
        # Close the files upon object destruction
        if self.simulation_file:
            self.simulation_file.close()
        if self.debug_file:
            self.debug_file.close()

    def simulation(self, message):
        with self.log_mutex:
            print(message, end='', flush=True)
            if self.simulation_file:
                self.simulation_file.write(message)
                self.simulation_file.flush()

            if self.debug_file:
                self.debug_file.write(message)
                self.debug_file.flush()

    def debug(self, message):
        with self.log_mutex:
            if self.debug_file:
                self.debug_file.write(message)
                self.debug_file.flush()

    def insert(self, message):
        with self.log_mutex:
            insert_file_name = os.path.join(self.directory, self.subdirectory, f"{self.name}_insert.txt")
            with open(insert_file_name, 'w') as insert_file:
                insert_file.write(message)

    def get_subdirectory(self):
        # Get the current date to use in the subdirectory
        now = datetime.datetime.now()
        return now.strftime("%Y_%m_%d")

    def get_simulation_directory(self):
        # Return a default directory, adjust as necessary
        return "simulations"

