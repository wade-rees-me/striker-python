import time
from sim.cards import Card
from sim.cards import Dealer
from sim.cards import Shoe
from sim.cards import deck_of_poker_cards
from sim.table import Rules
from sim.arguments import Parameters, Report
from .player import Player

STATUS_DOT = 25000;
STATUS_LINE = 1000000;

class Table:
    def __init__(self, index, parameters: Parameters):
        self.index = index
        self.parameters = parameters
        self.dealer = Dealer(parameters.rules.hit_soft_17)
        self.shoe = Shoe(deck_of_poker_cards, parameters.number_of_decks, parameters.rules.penetration)  # Create a new shoe object
        self.report = Report()
        self.player = None

    def add_player(self, player: Player):
        self.player = player

    def session(self, mimic):
        self.parameters.logger.simulation(f"      Start: table, playing {self.parameters.number_of_hands:,} hands\n");
        self.report.start = time.time()
        while self.report.total_hands < self.parameters.number_of_hands:
            self.status(self.report.total_rounds, self.report.total_hands)
            self.report.total_rounds += 1
            self.shoe.shuffle()
            self.player.shuffle()
            while not self.shoe.should_shuffle():
                self.report.total_hands += 1
                self.dealer.reset()
                self.player.place_bet(mimic)
                up_card = self.deal_cards()

                if not mimic and up_card.is_blackjack_ace():
                    self.player.insurance()

                if not self.dealer.hand.blackjack():  # Dealer does not have 21
                    self.player.play(mimic, self.shoe, up_card)
                    if not self.player.busted_or_blackjack():  # Dealer plays if player hasn't busted or blackjack
                        self.dealer.play(self.shoe)
                
                self.player.payoff(self.dealer.hand.blackjack(), self.dealer.hand.busted(), self.dealer.hand.total())
                self.show(up_card)

        self.report.end = time.time()
        self.report.duration = round(self.report.end - self.report.start)
        self.parameters.logger.simulation(f"\n      End: table\n")

    def deal_cards(self) -> Card:
        self.player.draw(self.shoe.draw())
        up_card = self.dealer.draw(self.shoe.draw())
        self.player.show(up_card)
        self.player.draw(self.shoe.draw())
        self.dealer.draw(self.shoe.draw())
        return up_card

    def show(self, up_card: Card):
        for card in self.dealer.hand.cards:
            if up_card.index != card.index:
                self.player.show(card)

    def status(self, round, hand):
        if round == 0:
            self.parameters.logger.simulation("        ")

        if (round + 1) % STATUS_DOT == 0:
            self.parameters.logger.simulation(".")

        if (round + 1) % STATUS_LINE == 0:
            #round_str = round + 1
            #hand_str = hand
            self.parameters.logger.simulation(f" : {round + 1:,} (rounds), {hand:,} (hands)\n")
            self.parameters.logger.simulation("        ")

