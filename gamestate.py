import csv
import random

class Card:
    def __init__(self, city_name, color):
        self.color = color
        self.city_name = city_name

class Deck:
    def __init__(self):
        with open("assets/CityCard_Types.csv", newline="") as city_color_file:
            reader = csv.reader(city_color_file, delimiter=",")
            next(reader)
            self.deck = [Card(row[0], row[1]) for row in reader]

    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.role =[]

class RoleCard:
    def __init__(self, role_type):
        self.role_type = role_type

class RoleCardDeck:
    def __init__(self):
        with open("assets/RoleCards.csv", newline="") as role_card_file:
            reader = csv.reader(role_card_file)
            self.role = [RoleCard(row[0]) for row in reader]

    def draw_role(self):
        r = random.choice(self.role)
        self.role.remove(r)
        return r

class GameState:
    def __init__(self):
        self.players = [] # list of Player objects
        self.is_game_mode = False
        self.deck = Deck()
        self.rolecarddeck = RoleCardDeck()

def add_player(state, player):
    state.players.append(player)

def remove_player(state, player):
    state.players.remove(player)

def start_game(state):
    state.is_game_mode = True
    size_init_hand = 4 if len(state.players) == 2 else 3 if len(state.players) == 3 else 2
    for player in state.players:
        player.role = state.rolecarddeck.draw_role()
        for _ in range(size_init_hand):
            player.hand.append(state.deck.draw_card())
