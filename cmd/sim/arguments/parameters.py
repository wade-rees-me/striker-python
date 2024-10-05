import time
import json
from sim.constants import STRIKER_WHO_AM_I

#
class Parameters:
    def __init__(self, name, decks, strategy, number_of_decks, number_of_hands, rules, logger):
        self.name = name
        self.decks = decks
        self.strategy = strategy
        self.number_of_decks = number_of_decks
        self.number_of_hands = number_of_hands
        self.rules = rules
        self.logger = logger
        self.playbook = f"{decks}-{strategy}"
        self.processor = STRIKER_WHO_AM_I
        self.timestamp = self.get_current_time()

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def print(self):
        self.logger.simulation(f"    {'Name':<24}: {self.name}\n")
        self.logger.simulation(f"    {'Playbook':<24}: {self.playbook}\n")
        self.logger.simulation(f"    {'Processor':<24}: {self.processor}\n")
        self.logger.simulation(f"    {'Version':<24}: {'STRIKER_VERSION'}\n")  # Replace with actual version constant
        self.logger.simulation(f"    {'Number of hands':<24}: {self.number_of_hands:,}\n")
        self.logger.simulation(f"    {'Timestamp':<24}: {self.timestamp}\n")

    def serialize(self):
        data = {
            "playbook": self.playbook,
            "name": self.name,
            "processor": self.processor,
            "timestamp": self.timestamp,
            "decks": self.decks,
            "strategy": self.strategy,
            "number_of_hands": self.number_of_hands,
            "number_of_decks": self.number_of_decks,
            "hit_soft_17": str(self.rules.hit_soft_17).lower(),
            "surrender": str(self.rules.surrender).lower(),
            "double_any_two_cards": str(self.rules.double_any_two_cards).lower(),
            "double_after_split": str(self.rules.double_after_split).lower(),
            "resplit_aces": str(self.rules.resplit_aces).lower(),
            "hit_split_aces": str(self.rules.hit_split_aces).lower(),
            "blackjack_bets": self.rules.blackjack_bets,
            "blackjack_pays": self.rules.blackjack_pays,
            "penetration": self.rules.penetration
        }
        return json.dumps(data, indent=4)

# Example usage
#if __name__ == "__main__":
#    rules = Rules()
#    logger = Logger()
#    params = Parameters("Example Simulation", "six-shoe", "basic", 6, 1000, rules, logger)
#    
#    # Print the parameters
#    params.print()
#
#    # Serialize to JSON
#    serialized_data = params.serialize()
#    print(serialized_data)

