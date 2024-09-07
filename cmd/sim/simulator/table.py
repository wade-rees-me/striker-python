import threading
import time
from sim.cards import Card
from sim.cards import Dealer
from sim.cards import Shoe
from sim.cards import deck_of_poker_cards
from sim.simulator import TableRules
from .simulation import SimulationParameters, SimulationReport
from .player import Player

class Table:
    def __init__(self, index, parameters: SimulationParameters):
        """
        Initialize a Table instance with dealer, player, shoe, and simulation parameters.
        :param index: Table index (unique ID)
        :param parameters: SimulationParameters object
        """
        self.index = index
        self.parameters = parameters
        self.dealer = Dealer(TableRules.hit_soft_17)
        self.shoe = Shoe(deck_of_poker_cards, parameters.number_of_decks, parameters.penetration)  # Create a new shoe object
        self.report = SimulationReport()
        self.player = None

    def add_player(self, player: Player):
        """
        Assign a player to the table.
        :param player: Player object
        """
        self.player = player

    def session(self):
        """
        Run a session of the simulation.
        """
        print(f"  Beg table {self.index:02d}: rounds: {self.parameters.rounds}")
        self.report.start = time.time()
        self.report.total_rounds = self.parameters.rounds
        for i in range(self.parameters.rounds):
            self.shoe.shuffle()
            self.player.shuffle()
            while not self.shoe.should_shuffle():
                self.report.total_hands += 1
                self.dealer.reset()
                self.player.place_bet()
                up_card = self.deal_cards()

                if up_card.is_blackjack_ace():
                    self.player.insurance()

                if not self.dealer.hand.blackjack():  # Dealer does not have 21
                    self.player.play(self.shoe, up_card)
                    if not self.player.busted_or_blackjack():  # Dealer plays if player hasn't busted or blackjack
                        self.dealer.play(self.shoe)
                
                self.player.payoff(self.dealer.hand.blackjack(), self.dealer.hand.busted(), self.dealer.hand.total())
                self.show(up_card)

        self.report.end = time.time()
        self.report.duration = round(self.report.end - self.report.start)
        print(f"  End table {self.index:02d}: ended at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.report.end))}, total elapsed time: {self.report.duration}s")

    def session_mimic(self):
        """
        Run a mimic session of the simulation.
        """
        print(f"  Beg table {self.index:02d} (mimic): rounds: {self.parameters.rounds}")
        self.report.start = time.time()
        self.report.total_rounds = self.parameters.rounds
        for i in range(self.parameters.rounds):
            self.shoe.shuffle()
            self.player.shuffle()
            while not self.shoe.should_shuffle():
                self.report.total_hands += 1
                self.dealer.reset()
                self.player.place_mimic_bet()
                up_card = self.deal_cards()

                if not self.dealer.hand.blackjack():
                    self.player.mimic_dealer(self.shoe)
                    if not self.player.busted_or_blackjack():
                        self.dealer.play(self.shoe)

                self.player.payoff(self.dealer.hand.blackjack(), self.dealer.hand.busted(), self.dealer.hand.total())

        self.report.end = time.time()
        self.report.duration = round(self.report.end - self.report.start)
        print(f"  End table {self.index:02d} (mimic): ended at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.report.end))}, total elapsed time: {self.report.duration}s")

    def deal_cards(self) -> Card:
        """
        Deal cards to the player and the dealer.
        :return: The dealer's face-up card
        """
        self.player.draw(self.shoe.draw())
        up_card = self.dealer.draw(self.shoe.draw())
        self.player.show(up_card)
        self.player.draw(self.shoe.draw())
        self.dealer.draw(self.shoe.draw())
        return up_card

    def show(self, up_card: Card):
        """
        Show the dealer's cards to the player, excluding the face-up card.
        :param up_card: The dealer's face-up card
        """
        for card in self.dealer.hand.cards:
            if up_card.index != card.index:
                self.player.show(card)

