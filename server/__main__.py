from threading import Thread, Lock
import socket

import jsonpickle

from shared import conn
from shared import gamestate



state_lock = Lock()
state = gamestate.GameState()

chat_connections = []

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
                if message.decode().startswith("chat"):
                    chat_msg = message.decode()[5:]
                    name = chat_msg[:chat_msg.find("|")-1]
                    msg = chat_msg[chat_msg.find("|")+1:]
                    for c in chat_connections:
                        conn.send_message(c, name.encode() + b": " + msg.encode())
                if message.decode() != "read":
                    print("received message: " + message.decode())
                if message.decode() == "start" and not state.is_game_mode:
                    with state_lock:
                        print("grabbed lock to start the game")
                        gamestate.start_game(state)
                    print("released lock")
                elif message.decode().startswith("joinlobby"):
                    self.player_name = message.decode()[10:]
                    print("message received: " + message.decode())
                    too_many_players = False
                    with state_lock:
                        print("grabbed lock to join lobby")
                        if len(state.players) < 4:
                            gamestate.add_player(state, gamestate.Player(self.player_name))
                            conn.send_message(self.conn, b'lobbyjoinsuccess')
                        else:
                            too_many_players = True
                    print("released lock")
                    if too_many_players:
                            conn.send_message(self.conn, b'toomanyplayers')
                elif message.decode() == "read":
                    with state_lock:
                        conn.send_message(self.conn, jsonpickle.encode(state).encode())
                else:
                    print("message not understood.")
            except conn.ConnectionClosed:
                with state_lock:
                    print("grabbed lock")
                    player = next(p for p in state.players if p.name == str(self.player_name))
                    gamestate.remove_player(state, player)
                print("released lock")
class Server:
    def __init__(self):
        PORT = 1066  # assigned randomly, any number of 1032

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # opening a TCP connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', PORT))  # telling the socket to use our host and port that we specified
        s.listen()  # only allowing one connection

        chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chat_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        chat_socket.bind(('', 1099))
        chat_socket.listen()

        print("listening on port " + str(PORT))

        num_conn = 0
        threads = []
        while not state.is_game_mode:
            conn, addr = s.accept()
            chat_conn, chat_addr = chat_socket.accept()
            chat_connections.append(chat_conn)
            print("Connection formed" + str(conn))
            t = ClientThread(conn, addr)
            t.start()
            threads.append(t)
            num_conn += 1

        print("done accepting connections!")
        while True:
            continue

s = Server()
