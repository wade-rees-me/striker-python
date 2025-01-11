import time
from striker.cards import Card
from striker.cards import Dealer
from striker.cards import Shoe
from striker.table import Rules
from striker.arguments import Parameters, Report
from .player import Player

STATUS_DOT = 25000;
STATUS_LINE = 1000000;

class Table:
    def __init__(self, index, parameters: Parameters, rules: Rules):
        self.index = index
        self.parameters = parameters
        self.dealer = Dealer(rules.hit_soft_17)
        self.shoe = Shoe(parameters.number_of_decks, rules.penetration)  # Create a new shoe object
        self.report = Report()
        self.player = None
        self.up_card = None
        self.down_card = None

    def add_player(self, player: Player):
        self.player = player

    def session(self, mimic):
        print(f"      Start: table, playing {self.parameters.number_of_hands:,} hands");
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
                self.deal_cards()

                if not mimic and self.up_card.is_blackjack_ace():
                    self.player.insurance()

                if not self.dealer.hand.blackjack():  # Dealer does not have 21
                    self.player.play(mimic, self.shoe, self.up_card)
                    if not self.player.busted_or_blackjack():  # Dealer plays if player hasn't busted or blackjack
                        while not self.dealer.stand():
                            card = self.shoe.draw();
                            self.dealer.draw(card);
                            self.player.show(card);
                
                self.player.show(self.down_card)
                self.player.payoff(self.dealer.hand.blackjack(), self.dealer.hand.busted(), self.dealer.hand.total())

        self.report.end = time.time()
        self.report.duration = round(self.report.end - self.report.start)
        print(f"\n      End: table")

    def deal_cards(self):
        self.player.draw(self.player.wager.hand, self.shoe)
        self.up_card = self.shoe.draw()
        self.dealer.draw(self.up_card)
        self.player.show(self.up_card)

        self.player.draw(self.player.wager.hand, self.shoe)
        self.down_card = self.shoe.draw()
        self.dealer.draw(self.down_card)

    def status(self, round, hand):
        if round == 0:
            print("        ", end="", flush=True)

        if (round + 1) % STATUS_DOT == 0:
            print(".", end="", flush=True)

        if (round + 1) % STATUS_LINE == 0:
            #round_str = round + 1
            #hand_str = hand
            print(f" : {round + 1:,} (rounds), {hand:,} (hands)")
            print("        ", end="", flush=True)

