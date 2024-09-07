from sim.cards import Wager, Shoe, Hand, Card
from sim.constants import MAX_SPLIT_HANDS, MINIMUM_BET
from sim.simulator import TableRules
from .simulation import SimulationParameters, SimulationReport
from .player_strategy import PlayerStrategy

class Player:
    def __init__(self, parameters, number_of_cards):
        """
        Initialize a Player instance with the necessary attributes.
        :param parameters: SimulationParameters object
        :param number_of_cards: Number of cards in the game
        """
        self.strategy = PlayerStrategy(parameters, number_of_cards)
        self.wager = Wager()
        self.splits = [Wager() for _ in range(MAX_SPLIT_HANDS)]
        self.split_count = 0
        self.blackjack_pays = 3
        self.blackjack_bets = 2
        self.parameters = parameters
        self.report = SimulationReport()
        self.number_of_cards = number_of_cards
        self.seen_cards = [0] * 13

        # Parse Blackjack payout
        try:
            self.blackjack_pays, self.blackjack_bets = map(int, parameters.blackjack_pays.split(':'))
        except ValueError as e:
            raise Exception(f"Failed to parse blackjack pays: {e}")

    def shuffle(self):
        """Reset seen cards."""
        self.seen_cards = [0] * 13

    def place_bet(self):
        """Reset the wager and place a bet."""
        self.wager.reset()
        for split in self.splits:
            split.reset()
        self.split_count = 0
        self.wager.bet(self.strategy.get_bet(self.seen_cards))

    def insurance(self):
        """Place an insurance bet if needed."""
        if self.strategy.get_insurance(self.seen_cards):
            self.wager.insurance_bet = self.wager.amount_bet // 2

    def play(self, shoe: Shoe, up: Card):
        """Play a hand against the dealer."""
        if self.wager.hand.blackjack():
            return

        have_cards = self.get_have(self.wager.hand)
        if self.strategy.get_surrender(have_cards, up.offset, self.seen_cards):
            self.wager.hand.surrender = True
            return

        if self.strategy.get_double(have_cards, up.offset, self.seen_cards) and \
           (TableRules.double_any_two_cards or self.wager.hand.total() in {10, 11}):
            self.wager.double()
            self.wager.hand.draw(shoe.draw())
            return

        if self.wager.hand.pair() and self.strategy.get_split(self.wager.hand.cards[0].value, up.offset, self.seen_cards):
            split = self.splits[self.split_count]
            self.split_count += 1
            if self.wager.hand.pair_of_aces():
                if not TableRules.resplit_aces and not TableRules.hit_split_aces:
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

        while not self.wager.hand.busted() and not self.strategy.get_stand(have_cards, up.offset, self.seen_cards):
            self.wager.hand.draw(shoe.draw())
            have_cards = self.get_have(self.wager.hand)

    def play_split(self, wager: Wager, shoe: Shoe, up: Card):
        """Play a split hand."""
        have_cards = self.get_have(wager.hand)
        if TableRules.double_after_split and self.strategy.get_double(have_cards, up.offset, self.seen_cards):
            wager.double()
            wager.hand.draw(shoe.draw())
            return

        if wager.hand.pair() and self.split_count < MAX_SPLIT_HANDS:
            if self.strategy.get_split(wager.hand.cards[0].value, up.offset, self.seen_cards):
                if not wager.hand.pair_of_aces() or \
                   (wager.hand.pair_of_aces() and TableRules.resplit_aces):
                    split = self.splits[self.split_count]
                    self.split_count += 1
                    wager.split_wager(split)
                    wager.hand.draw(shoe.draw())
                    self.play_split(wager, shoe, up)
                    split.hand.draw(shoe.draw())
                    self.play_split(split, shoe, up)
                    return

        if wager.hand.cards[0].is_blackjack_ace() and not TableRules.hit_split_aces:
            return

        while not wager.hand.busted() and not self.strategy.get_stand(have_cards, up.offset, self.seen_cards):
            wager.hand.draw(shoe.draw())
            have_cards = self.get_have(wager.hand)

    def draw(self, card: Card) -> Card:
        """Draw a card and update seen cards."""
        self.show(card)
        return self.wager.hand.draw(card)

    def show(self, card: Card):
        """Track the card drawn."""
        self.seen_cards[card.offset] += 1

    def busted_or_blackjack(self) -> bool:
        """Check if the player busted or has blackjack."""
        if self.split_count == 0:
            return self.wager.hand.busted() or self.wager.hand.blackjack()

        if not self.wager.hand.busted():
            return False

        return all(split.hand.busted() for split in self.splits[:self.split_count])

    def payoff(self, dealer_blackjack: bool, dealer_busted: bool, dealer_total: int):
        """Calculate the payoff based on the dealer's outcome."""
        if self.split_count == 0:
            self.payoff_hand(self.wager, dealer_blackjack, dealer_busted, dealer_total)
        else:
            self.payoff_split(self.wager, dealer_busted, dealer_total)
            for split in self.splits[:self.split_count]:
                self.payoff_split(split, dealer_busted, dealer_total)

    def payoff_hand(self, wager: Wager, dealer_blackjack: bool, dealer_busted: bool, dealer_total: int):
        """Payoff for a single hand."""
        if dealer_blackjack:
            wager.won_insurance()
        else:
            wager.lost_insurance()

        if wager.hand.surrender:
            self.report.total_won -= wager.amount_bet // 2
        else:
            if dealer_blackjack:
                if wager.hand.blackjack():
                    wager.push()
                else:
                    wager.lost()
            elif wager.hand.blackjack():
                wager.won_blackjack(self.blackjack_pays, self.blackjack_bets)
            elif wager.hand.busted():
                wager.lost()
            elif dealer_busted or wager.hand.total() > dealer_total:
                wager.won()
            elif dealer_total > wager.hand.total():
                wager.lost()
            else:
                wager.push()

        self.report.total_won += wager.amount_won + wager.double_won
        self.report.total_bet += wager.amount_bet + wager.double_bet + wager.insurance_bet

    def payoff_split(self, wager: Wager, dealer_busted: bool, dealer_total: int):
        """Payoff for a split hand."""
        if wager.hand.busted():
            wager.lost()
        elif dealer_busted or wager.hand.total() > dealer_total:
            wager.won()
        elif dealer_total > wager.hand.total():
            wager.lost()
        else:
            wager.push()

        self.report.total_won += wager.amount_won + wager.double_won
        self.report.total_bet += wager.amount_bet + wager.double_bet

    def get_have(self, hand: Hand) -> list:
        """Track the cards in hand."""
        have_cards = [0] * 13
        for card in hand.cards:
            have_cards[card.offset] += 1
        return have_cards

    def place_mimic_bet(self):
        """
        Resets the player's wager and places a minimum bet.
        """
        self.wager.reset()
        self.wager.bet(MINIMUM_BET)

    def mimic_dealer(self, shoe: Shoe):
        """
        The player draws cards until they should stand.
        :param shoe: Shoe object from which cards are drawn.
        """
        while not self.mimic_stand():
            self.draw(shoe.draw())

    def mimic_stand(self):
        """
        Determines if the player should stand based on the hand's value.
        :return: True if the player should stand, False otherwise.
        """
        if self.wager.hand.soft_17():
            return False
        return self.wager.hand.total() >= 17
