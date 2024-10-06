from sim.cards import Wager, Shoe, Hand, Card, MINIMUM_BET
from sim.constants import MAX_SPLIT_HANDS
from sim.table import Rules
from sim.arguments import Parameters, Report
from .strategy import Strategy

class Player:
    def __init__(self, parameters, number_of_cards):
        self.strategy = Strategy(parameters.playbook, number_of_cards)
        self.wager = Wager()
        self.splits = [Wager() for _ in range(MAX_SPLIT_HANDS)]
        self.split_count = 0
        self.parameters = parameters
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
            return

        if mimic:
            while not self.mimic_stand():
                self.draw(shoe.draw())
            return

        self.strategy.do_play(self.seen_cards, self.get_have(self.wager.hand), self.wager.hand.cards[0] if self.wager.hand.pair() else None, up)
        if self.parameters.rules.surrender and self.strategy.get_surrender(self.seen_cards, self.get_have(self.wager.hand), up):
            self.wager.hand.surrender = True
            return

        if (self.parameters.rules.double_any_two_cards or self.wager.hand.total() in {10, 11}) and self.strategy.get_double(self.seen_cards, self.get_have(self.wager.hand), up):
            self.wager.double()
            self.wager.hand.draw(shoe.draw())
            return

        if self.wager.hand.pair() and self.strategy.get_split(self.seen_cards, self.wager.hand.cards[0], up):
            split = self.splits[self.split_count]
            self.split_count += 1
            if self.wager.hand.pair_of_aces():
                if not self.parameters.rules.resplit_aces and not self.parameters.rules.hit_split_aces:
                    self.wager.split_wager(split)
                    self.wager.hand.draw(shoe.draw())
                    split.hand.draw(shoe.draw())
                    return
            self.wager.split_wager(split)
            self.wager.hand.draw(shoe.draw())
            self.play_split(self.wager, shoe, up)
            split.hand.draw(shoe.draw())
            self.play_split(split, shoe, up)
            return

        while not self.wager.hand.busted() and not self.strategy.get_stand(self.seen_cards, self.get_have(self.wager.hand), up):
            self.wager.hand.draw(shoe.draw())
            #have_cards = self.get_have(self.wager.hand)

    def play_split(self, wager: Wager, shoe: Shoe, up: Card):
        have_cards = self.get_have(wager.hand)
        if self.parameters.rules.double_after_split and self.strategy.get_double(self.seen_cards, have_cards, up):
            wager.double()
            wager.hand.draw(shoe.draw())
            return

        if wager.hand.pair() and self.split_count < MAX_SPLIT_HANDS:
            if self.strategy.get_split(self.seen_cards, wager.hand.cards[0], up):
                if not wager.hand.pair_of_aces() or \
                   (wager.hand.pair_of_aces() and self.parameters.rules.resplit_aces):
                    split = self.splits[self.split_count]
                    self.split_count += 1
                    wager.split_wager(split)
                    wager.hand.draw(shoe.draw())
                    self.play_split(wager, shoe, up)
                    split.hand.draw(shoe.draw())
                    self.play_split(split, shoe, up)
                    return

        if wager.hand.cards[0].is_blackjack_ace() and not self.parameters.rules.hit_split_aces:
            return

        while not wager.hand.busted() and not self.strategy.get_stand(self.seen_cards, have_cards, up):
            wager.hand.draw(shoe.draw())
            have_cards = self.get_have(wager.hand)

    def draw(self, card: Card) -> Card:
        self.show(card)
        return self.wager.hand.draw(card)

    def show(self, card: Card):
        self.seen_cards[card.get_offset()] += 1

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

        if wager.hand.surrender:
            self.report.total_won -= wager.amount_bet // 2
        else:
            #print(f"player:{wager.hand.total()}, dealer:{dealer_total}")
            if dealer_blackjack:
                if wager.hand.blackjack():
                    wager.push()
                else:
                    wager.lost()
            elif wager.hand.blackjack():
                wager.won_blackjack(self.parameters.rules.blackjack_pays, self.parameters.rules.blackjack_bets)
            elif wager.hand.busted():
                wager.lost()
            elif dealer_busted or wager.hand.total() > dealer_total:
                wager.won()
            elif dealer_total > wager.hand.total():
                wager.lost()
            else:
                wager.push()

        self.report.total_won += wager.amount_won
        self.report.total_bet += wager.amount_bet + wager.insurance_bet

    def payoff_split(self, wager: Wager, dealer_busted: bool, dealer_total: int):
        if wager.hand.busted():
            wager.lost()
        elif dealer_busted or wager.hand.total() > dealer_total:
            wager.won()
        elif dealer_total > wager.hand.total():
            wager.lost()
        else:
            wager.push()

        self.report.total_won += wager.amount_won
        self.report.total_bet += wager.amount_bet

    def get_have(self, hand: Hand) -> list:
        have_cards = [0] * 13
        for card in hand.cards:
            have_cards[card.get_offset()] += 1
        return have_cards

    def mimic_stand(self):
        if self.wager.hand.soft_17():
            return False
        return self.wager.hand.total() >= 17

