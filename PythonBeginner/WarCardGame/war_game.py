from card_deck import *
import random
TOTAL_PLAYERS = 4


class Player:
    def __init__(self, identifier):
        self.deck = []
        self.win_pile = []
        self.identifier = identifier

    def give_card(self, card):
        card.owner = self.identifier
        self.deck.append(card)

    def give_to_win_pile(self, cards):
        for i in range(0, len(cards)):
            cards[i].owner = self.identifier
        self.win_pile = self.win_pile + cards

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def top_card(self):
        return self.deck.pop()

    def merge_pile(self):
        self.deck = self.deck + self.win_pile
        self.shuffle_deck()
        self.win_pile = []

    def print_deck(self):
        for i in range(0, len(self.deck)):
            self.deck[i].print_name()

    def print_win_pile(self):
        for i in range(0, len(self.win_pile)):
            self.win_pile[i].print_name()

    def is_out(self):
        return (len(self.deck) + len(self.win_pile)) == 0


def get_owner(card, players):
    for i in range(0, len(players)):
        if (card.owner == players[i].identifier):
            return players[i]


def get_player(players, id):
    for i in range(0, len(players)):
        if (players[i].identifier == id):
            return players[i]


def play_top_card(pot, war_mates=[]):
    global TOTAL_PLAYERS
    global players
    if (len(war_mates) > 1):
        for i in range(0, len(war_mates)):
            temp_p = get_player(players, war_mates[i])
            print("war revealing for player" + str(war_mates[i]))
            pot.append(temp_p.top_card())
            print("Player" + str(temp_p.identifier) + " reveals the card " + pot[len(pot) - 1].name())
    else:
        for i in range(0, TOTAL_PLAYERS):
            if (players[i].is_out()):
                continue
            pot.append(players[i].top_card())
            print("Player" + str(i) + " reveals the card " + pot[len(pot) - 1].name())


## Create game objects
deck = create_deck()
players = []
for i in range(0, TOTAL_PLAYERS):
    players.append(Player(i))

# deal out the deck
deal_deck(deck, players, TOTAL_PLAYERS)
g_pot = []
has_won = False
war_count = 0


def play_round(war_mates=[]):
    global war_count
    global players
    global g_pot
    pot = []
    # each player reveals the top card of their decks
    if len(war_mates) <= 1:
        play_top_card(pot)
    else:
        play_top_card(pot, war_mates)

    # higher card wins and goes to winners win pile
    pot.sort(key=lambda x: x.number, reverse=True)

    # check for a war amongst players
    highest = pot[0].card_value()
    war_mates = [pot[0].owner]
    for i in range(1, len(pot)):
        if (pot[i].card_value() == highest):
            war_mates.append(pot[i].owner)
            print("Player" + str(pot[i].owner) + " joins the war against Player" + str(pot[0].owner))
        else:
            break

    if (len(war_mates) > 1):
        # Each involved mills 3 cards
        for i in range(len(war_mates) - 1, -1, -1):
            temp_p = get_player(players, war_mates[i])
            # make sure you have 3 to mill
            if (len(temp_p.deck) + len(temp_p.win_pile) < 4):
                # forfeit war if not enough cards to wage the war
                print("Player" + str(war_mates[i]) + " doesn't have cards to conduct the war")
                war_mates = war_mates[:i] + war_mates[i + 1:]
                continue
            elif (len(temp_p.deck) <= 4):
                # shuffle in win pile to make the 3 card cost + flip cost
                temp_p.merge_pile()
                temp_p.shuffle_deck()
                war_count += 1
            else:
                war_count += 1
            g_pot.append(temp_p.top_card())
            g_pot.append(temp_p.top_card())
            g_pot.append(temp_p.top_card())
        # Reveals 3, and the winner takes all
        # iff there are warmates left
        if (len(war_mates) <= 1):
            # Give the winner the pot
            g_pot = g_pot + pot
            winner = get_player(players, war_mates[0])
            winner.give_to_win_pile(g_pot)
            print("default winner for pot of " + str(len(g_pot)))
            g_pot = []
        else:
            # We have a war
            g_pot = g_pot + pot
            play_round(war_mates)
    else:
        # Give the winner the pot
        g_pot = g_pot + pot
        winner = get_owner(pot[0], players)
        winner.give_to_win_pile(g_pot)
        g_pot = []


## the war game
round_count = 0
while (not (has_won)):
    round_count += 1
    print("Round " + str(round_count))
    print("=====================")
    play_round()

    ## End of turn procedures
    # when a player is out of cards in their deck, shuffle win pile into the deck
    for i in range(0, TOTAL_PLAYERS):
        if (len(players[i].deck) < 1 and len(players[i].win_pile) > 0):
            players[i].deck = players[i].win_pile
            players[i].shuffle_deck()
            players[i].win_pile = []
        # if someone has all the cards in the game, they have won
        if (len(players[i].deck) + len(players[i].win_pile) == 52):
            print("GAME OVER, PLAYER" + str(i) + " HAS WON THE GAME AFTER " + str(round_count) + " ROUNDS & " + str(
                war_count) + " WARS.")
            has_won = True
            break;
        print("Player" + str(i) + " has " + str(len(players[i].deck) + len(players[i].win_pile)) + " cards left.")
    print("=====================\n")
