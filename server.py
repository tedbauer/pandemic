import conn
import random
import csv
import socket
import jsonpickle
from threading import Thread, Lock

# deal cards to beginning players
# 2-4 players; each player gets a deck of cards

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

class GameState:
    def __init__(self):
        self.players = [] # list of Player objects
        self.is_game_mode = False
        self.deck = Deck()

        self.lock = Lock()

    def add_player(self, player):
        with self.lock:
            self.players.append(player)

    def remove_player(self, player):
        with self.lock:
            self.players.remove(player)

    def start_game(self):
        with self.lock:
            self.is_game_mode = True
            size_init_hand = 4 if len(self.players) == 2 else 3 if len(self.players) == 3 else 2
            for player in self.players:
                for _ in range(size_init_hand):
                    player.hand.append(self.deck.draw_card())

class ClientThread(Thread):
    def __init__(self, conn, addr, state, player_nbr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.state = state
        self.player_nbr = player_nbr

    def run(self):
        while True:
            try:
                message = conn.receive_message(self.conn)
                if message.decode() == "start" and not self.state.is_game_mode:
                    self.state.start_game()
                elif message.decode() == "read":
                    conn.send_message(self.conn, jsonpickle.encode(self.state).encode())
            except conn.ConnectionClosed:
                player = next(p for p in self.state.players if p.name == str(self.player_nbr))
                self.state.remove_player(player)


class Server:
    def __init__(self):
        PORT = 1066  # assigned randomly, any number of 1032

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # opening a TCP connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind(('', PORT))  # telling the socket to use our host and port that we specified
        s.listen()  # only allowing one connection

        print("listening on port " + str(PORT))

        num_conn = 0
        threads = []
        state = GameState()
        while not state.is_game_mode:
            conn, addr = s.accept()
            print("Connection formed" + str(conn))
            t = ClientThread(conn, addr, state, num_conn)
            state.add_player(Player(str(num_conn)))
            t.start()
            threads.append(t)
            num_conn += 1

s = Server()
