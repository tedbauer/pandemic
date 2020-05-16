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
        data_buffer = b''
        while True:
            print(data_buffer)
            new_data = self.conn.recv(1024)
            print(new_data)
            data_buffer += new_data
            if b'\0' in data_buffer:
                message_buffer = data_buffer[:data_buffer.rfind(b'\0')]
                messages = message_buffer.split(b'\0')
                data_buffer = data_buffer[data_buffer.rfind(b'\0'):]
                for msg in messages:
                    print(msg)
                    if msg.decode() == "start" and not self.state.is_game_mode:
                        print("starting game")
                        self.state.start_game()
                    elif msg.decode() == "read":
                        print("performing read")
                        self.conn.sendall((jsonpickle.encode(self.state) + '\0').encode())
            if not new_data:
                break
        self.conn.close()

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
