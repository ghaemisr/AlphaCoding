import random


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        self.owner = None

    def name(self):
        name = ""
        if self.number <= 10:
            name += str(self.number)
        elif self.number == 11:
            name += "Jack"
        elif self.number == 12:
            name += "Queen"
        elif self.number == 13:
            name += "King"
        elif self.number == 14:
            name += "Ace"
        name += "of" + self.suit
        return name

    def print_name(self):
        print(self.name())

    def card_value(self):
        return self.number


def create_deck():
    deck = []
    suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
    numbers = range(2, 15)

    for suit in suits:
        for number in numbers:
            deck.append(Card(suit, number))

    return deck


def deal_deck(deck, players, players_max):
    current_player = 0
    while len(deck) > 0:
        rand = random.randint(0, len(deck)-1)
        rand_card = deck[rand]
        deck = deck[:rand] + deck[rand + 1:]
        players[current_player].give_card(rand_card)
        current_player += 1
        if current_player >= players_max:
            current_player = 0

