from socket import socket, AF_INET, SOCK_STREAM

from shared import conn

class ChatChannel:
    def __init__(self, ip, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((ip, port))

    def get_chat_message(self):
        return conn.receive_message(self.socket).decode()
