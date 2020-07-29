from threading import Lock
from socket import socket, AF_INET, SOCK_STREAM

import jsonpickle

from shared import conn

class ServerChannel:
    def __init__(self, ip, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((ip, port))

        self.send_message_lock = Lock()

    def read_new_state(self):
        with self.send_message_lock:
            conn.send_message(self.socket, b'read')
        return jsonpickle.decode(conn.receive_message(self.socket))

    def join_lobby(self, name):
        with self.send_message_lock:
            conn.send_message(self.socket, b'joinlobby|' + name.encode())
        response = conn.receive_message(self.socket).decode()
        if response == "toomanyplayers":
            print("too many players have already joined this lobby")
            exit(0)
        elif response == "lobbyjoinsuccess":
            print("joined lobby")
        else:
            print("unknown response from server: " + response)
            exit(1)

    def request_game_start(self):
        with self.send_message_lock:
            conn.send_message(self.socket, b'start')

    def send_chat_msg(self, name, msg):
        with self.send_message_lock:
            conn.send_message(self.socket, b'chat|' + name.encode() + b'|' + msg.encode())
