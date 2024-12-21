from .card import Card, new_card
import random

# Shoe class represents a collection of cards
class Shoe:
    def __init__(self, number_of_decks, penetration):
        self.cards = []
        self.force_shuffle = False
        self.number_of_cards = 0
        self.cut_card = 0
        self.burn_card = 1
        self.next_card = 0
        self.last_discard = 0

        suits = ["spades", "diamonds", "clubs", "hearts"]
        card_names = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
        card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        card_keys = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        # Populate the shoe with cards
        for _ in range(number_of_decks):
            for suit in suits:
                for idx, name in enumerate(card_names):
                    self.cards.append(new_card(suit, name, card_keys[idx], card_values[idx], idx))
        
        self.number_of_cards = len(self.cards)
        self.cut_card = int(self.number_of_cards * penetration)
        self.next_card = self.number_of_cards
        self.last_discard = self.number_of_cards

        random.seed()
        self.shuffle()

    def shuffle(self):
        self.last_discard = self.number_of_cards
        self.force_shuffle = False
        self.shuffle_random()

    def shuffle_random(self):
        random.shuffle(self.cards)
        self.next_card = self.burn_card

    def draw(self):
        if self.next_card >= self.number_of_cards:
            self.force_shuffle = True
            self.shuffle_random()
        card = self.cards[self.next_card]
        self.next_card += 1
        return card

    def should_shuffle(self):
        self.last_discard = self.next_card
        return (self.next_card >= self.cut_card) or self.force_shuffle

    def display(self):
        print("-" * 80)
        for idx, card in enumerate(self.cards):
            print(f"{idx:03}: ", end="")
            card.display()
        print("-" * 80)

