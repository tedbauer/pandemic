from socket import socket, AF_INET, SOCK_STREAM

import jsonpickle

from shared import conn

class ServerChannel:
    def __init__(self, ip, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((ip, port))

    def read_new_state(self):
        conn.send_message(self.socket, b'read')
        return jsonpickle.decode(conn.receive_message(self.socket))

    def join_lobby(self, name):
        conn.send_message(self.socket, b'joinlobby|' + name.encode())

    def request_game_start(self): pass
