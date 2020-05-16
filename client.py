import socket
import pygame
import jsonpickle

class Client:

    def __init__(self, ip):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, 1066))

        self.socket.sendall("start\0".encode())
        self.socket.sendall("read\0".encode())
        data_buffer = b''
        while True:
            print("THIS ITERATION HAPPEND")
            new_data = self.socket.recv(1024)
            data_buffer += new_data
            if b'\0' in data_buffer:
                message_buffer = data_buffer[:data_buffer.rfind(b'\0')]
                messages = message_buffer.split(b'\0')
                data_buffer = data_buffer[data_buffer.rfind(b'\0'):]
                for msg in messages:
                    game_state = jsonpickle.decode(msg.decode())
                    print([card["city_name"] for card in game_state["players"][0]["hand"]])
            if not new_data: break

        screen = pygame.display.set_mode((640, 480))
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == '__main__':

    ip = input("Enter server IP address:")
    client = Client(ip)
