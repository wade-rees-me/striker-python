import time
import sys
from striker.cards import Card
from striker.cards import Dealer
from striker.cards import Shoe
from striker.table import Rules
from striker.arguments import Parameters, Report
from striker.constants import STATUS_ROUNDS
from striker.shared import SharedValue
from .player import Player


class Table:
    def __init__(self, core, parameters: Parameters, rules: Rules):
        self.core = core
        self.parameters = parameters
        self.dealer = Dealer(rules.hit_soft_17)
        self.shoe = Shoe(
            parameters.number_of_decks, rules.penetration
        )  # create a new shoe object
        self.report = Report()
        self.player = None
        self.up_card = None
        self.down_card = None

    def add_player(self, player: Player):
        self.player = player

    def session(self, mimic):
        self.report.start = time.time()
        while self.report.total_hands.get() < self.parameters.share_of_hands.get():
            if self.parameters.verbose:
                self.status(self.report.total_rounds, self.report.total_hands)
            self.report.total_rounds.inc()
            self.shoe.shuffle()
            self.player.shuffle()
            while not self.shoe.should_shuffle():
                self.report.total_hands.inc()
                self.dealer.reset()
                self.player.place_bet(mimic)
                self.deal_cards()

                if not mimic and self.up_card.is_blackjack_ace():
                    self.player.insurance()

                if not self.dealer.hand.blackjack():  # dealer does not have 21
                    self.player.play(mimic, self.shoe, self.up_card)
                    if (
                        not self.player.busted_or_blackjack()
                    ):  # dealer plays if player hasn't busted or blackjack
                        while not self.dealer.stand():
                            card = self.shoe.draw()
                            self.dealer.draw(card)
                            self.player.show(card)

                self.player.show(self.down_card)
                self.player.payoff(
                    self.dealer.hand.blackjack(),
                    self.dealer.hand.busted(),
                    self.dealer.hand.total(),
                )
        print(f"\r", end="")

    def deal_cards(self):
        self.player.draw(self.player.wager.hand, self.shoe)
        self.up_card = self.shoe.draw()
        self.dealer.draw(self.up_card)
        self.player.show(self.up_card)

        self.player.draw(self.player.wager.hand, self.shoe)
        self.down_card = self.shoe.draw()
        self.dealer.draw(self.down_card)

    def status(self, round, hand):
        if round.get() % STATUS_ROUNDS == 0:
            print(
                f"\r    Rounds: [{round.get():<13,}]: Hands: [{hand.get():<13,}]: Simulating...",
                end="",
                flush=True,
            )
