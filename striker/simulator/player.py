#from striker.cards import Wager, Shoe, Hand, Card, MINIMUM_BET
from striker.cards import Wager, Shoe, Hand, Card
from striker.constants import MAX_SPLIT_HANDS, MINIMUM_BET, MAXIMUM_BET
from striker.table import Rules, Strategy
from striker.arguments import Parameters, Report

class Player:
    def __init__(self, parameters, rules, strategy, number_of_cards):
        self.wager = Wager(MINIMUM_BET, MAXIMUM_BET)
        self.splits = [Wager(MINIMUM_BET, MAXIMUM_BET) for _ in range(MAX_SPLIT_HANDS)]
        self.split_count = 0
        self.parameters = parameters
        self.rules = rules
        self.strategy = strategy
        self.report = Report()
        self.number_of_cards = number_of_cards
        self.seen_cards = [0] * 13

    def shuffle(self):
        self.seen_cards = [0] * 13

    def place_bet(self, mimic):
        self.wager.reset()
        for split in self.splits:
            split.reset()
        self.split_count = 0
        if mimic:
            self.wager.bet(MINIMUM_BET)
        else:
            self.wager.bet(self.strategy.get_bet(self.seen_cards))

    def insurance(self):
        if self.strategy.get_insurance(self.seen_cards):
            self.wager.insurance_bet = self.wager.amount_bet // 2

    def play(self, mimic, shoe: Shoe, up: Card):
        if self.wager.hand.blackjack():
            self.report.total_blackjacks += 1
            return

        if mimic:
            while not self.mimic_stand():
                self.draw(self.wager.hand, shoe)
            return

        if self.strategy.get_double(self.seen_cards, self.wager.hand.total(), self.wager.hand.soft(), up):
            self.wager.double()
            self.draw(self.wager.hand, shoe)
            self.report.total_doubles += 1
            return

        if self.wager.hand.pair() and self.strategy.get_split(self.seen_cards, self.wager.hand.cards[0], up):
            split = self.splits[self.split_count]
            self.split_count += 1
            self.report.total_splits += 1
            if self.wager.hand.pair_of_aces():
                self.wager.split_wager(split)
                self.draw(self.wager.hand, shoe)
                self.draw(split.hand, shoe)
                return
            self.wager.split_wager(split)
            self.draw(self.wager.hand, shoe)
            self.play_split(self.wager, shoe, up)
            self.draw(split.hand, shoe)
            self.play_split(split, shoe, up)
            return

        do_stand = self.strategy.get_stand(self.seen_cards, self.wager.hand.total(), self.wager.hand.soft(), up)
        while not self.wager.hand.busted() and not do_stand:
            self.draw(self.wager.hand, shoe)
            if not self.wager.hand.busted():
                do_stand = self.strategy.get_stand(self.seen_cards, self.wager.hand.total(), self.wager.hand.soft(), up)

    def play_split(self, wager: Wager, shoe: Shoe, up: Card):
        if wager.hand.pair() and self.split_count < MAX_SPLIT_HANDS:
            if self.strategy.get_split(self.seen_cards, wager.hand.cards[0], up):
                split = self.splits[self.split_count]
                self.split_count += 1
                self.report.total_splits += 1
                wager.split_wager(split)
                self.draw(wager.hand, shoe)
                self.play_split(wager, shoe, up)
                self.draw(split.hand, shoe)
                self.play_split(split, shoe, up)
                return

        do_stand = self.strategy.get_stand(self.seen_cards, wager.hand.total(), wager.hand.soft(), up)
        while not wager.hand.busted() and not do_stand:
            self.draw(wager.hand, shoe)
            if not wager.hand.busted():
                do_stand = self.strategy.get_stand(self.seen_cards, wager.hand.total(), wager.hand.soft(), up)

    def draw(self, hand: Hand, shoe: Shoe) -> Card:
        card = shoe.draw()
        self.show(card)
        hand.draw(card)
        return card

    def show(self, card: Card):
        self.seen_cards[card.get_value()] += 1

    def busted_or_blackjack(self) -> bool:
        if self.split_count == 0:
            return self.wager.hand.busted() or self.wager.hand.blackjack()

        if not self.wager.hand.busted():
            return False

        return all(split.hand.busted() for split in self.splits[:self.split_count])

    def payoff(self, dealer_blackjack: bool, dealer_busted: bool, dealer_total: int):
        if self.split_count == 0:
            self.payoff_hand(self.wager, dealer_blackjack, dealer_busted, dealer_total)
        else:
            self.payoff_split(self.wager, dealer_busted, dealer_total)
            for split in self.splits[:self.split_count]:
                self.payoff_split(split, dealer_busted, dealer_total)

    def payoff_hand(self, wager: Wager, dealer_blackjack: bool, dealer_busted: bool, dealer_total: int):
        if dealer_blackjack:
            wager.won_insurance()
        else:
            wager.lost_insurance()

        #print(f"player:{wager.hand.total()}, dealer:{dealer_total}")
        if dealer_blackjack:
            if wager.hand.blackjack():
                wager.push()
                self.report.total_pushes += 1
            else:
                wager.lost()
                self.report.total_loses += 1
        elif wager.hand.blackjack():
            wager.won_blackjack(self.rules.blackjack_pays, self.rules.blackjack_bets)
        elif wager.hand.busted():
            wager.lost()
            self.report.total_loses += 1
        elif dealer_busted or wager.hand.total() > dealer_total:
            wager.won()
            self.report.total_wins += 1
        elif dealer_total > wager.hand.total():
            wager.lost()
            self.report.total_loses += 1
        else:
            wager.push()
            self.report.total_pushes += 1

        self.report.total_won += wager.amount_won
        self.report.total_bet += wager.amount_bet + wager.insurance_bet

    def payoff_split(self, wager: Wager, dealer_busted: bool, dealer_total: int):
        if wager.hand.busted():
            wager.lost()
            self.report.total_loses += 1
        elif dealer_busted or wager.hand.total() > dealer_total:
            wager.won()
            self.report.total_wins += 1
        elif dealer_total > wager.hand.total():
            wager.lost()
            self.report.total_loses += 1
        else:
            wager.push()
            self.report.total_pushes += 1

        self.report.total_won += wager.amount_won
        self.report.total_bet += wager.amount_bet

    def mimic_stand(self):
        if self.wager.hand.soft_17():
            return False
        return self.wager.hand.total() >= 17

