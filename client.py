import conn
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
        while running:
            screen.fill((0,0,0))
            text_surface = font.render("Lobby", True, (255,255,255))
            screen.blit(text_surface, dest=(5, 5))
            conn.send_message(self.socket, b'read')

            game_state = jsonpickle.decode(conn.receive_message(self.socket))
            players = game_state["players"]
            for i in range(len(players)):
                text_surface = font.render("- player " + players[i]["name"], True, (255,255,255))
                screen.blit(text_surface, dest=(50, 50+i*50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == '__main__':
    ip = input("Enter server IP address:")
    client = Client(ip)
