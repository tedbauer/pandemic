import socket
import pygame
import jsonpickle

class Client:

    def __init__(self, ip):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, 1066))

        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        screen.fill((0,0,0))
        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        running = True
        data_buffer = b''
        while running:
            screen.fill((0,0,0))
            text_surface = font.render("Lobby", True, (255,255,255))
            screen.blit(text_surface, dest=(5, 5))
            self.socket.sendall("read\0".encode())

            grabbing_data = True
            while grabbing_data:
                new_data = self.socket.recv(1024)
                if not new_data: break
                data_buffer += new_data
                if b'\0' in data_buffer:
                    message_buffer = data_buffer[:data_buffer.rfind(b'\0')]
                    messages = message_buffer.split(b'\0')
                    data_buffer = data_buffer[data_buffer.rfind(b'\0')+1:]
                    for msg in messages:
                        game_state = jsonpickle.decode(msg)
                        players = game_state["players"]
                        for i in range(len(players)):
                            text_surface = font.render("- player " + players[i]["name"], True, (255,255,255))
                            screen.blit(text_surface, dest=(50, 50+i*50))
                    grabbing_data = False

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == '__main__':
    ip = input("Enter server IP address:")
    client = Client(ip)
