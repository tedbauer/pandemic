import conn
import random
import csv
import socket
import jsonpickle
from threading import Thread, Lock
import gamestate

# deal cards to beginning players
# 2-4 players; each player gets a deck of cards

state_lock = Lock()
state = gamestate.GameState()

class ClientThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.player_name = None

    def run(self):
        while True:
            try:
                message = conn.receive_message(self.conn)
                if message.decode() == "start" and not state.is_game_mode:
                    with state_lock:
                        gamestate.start_game(state)
                elif message.decode().startswith("setname"):
                    self.player_name = message.decode()[8:]
                    with state_lock:
                        gamestate.add_player(state, gamestate.Player(self.player_name))
                elif message.decode() == "read":
                    with state_lock:
                        conn.send_message(self.conn, jsonpickle.encode(state).encode())
            except conn.ConnectionClosed:
                with state_lock:
                    player = next(p for p in state.players if p.name == str(self.player_name))
                    gamestate.remove_player(state, player)

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
        while not state.is_game_mode:
            conn, addr = s.accept()
            print("Connection formed" + str(conn))
            t = ClientThread(conn, addr)
            t.start()
            threads.append(t)
            num_conn += 1

        print("done accepting connections!")
        while True:
            continue

s = Server()
