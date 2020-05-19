import conn
import socket
import pygame
import jsonpickle

class Client:

    def __init__(self, ip, name):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, 1066))

        pygame.init()
        screen = pygame.display.set_mode((1000, 800))
        screen.fill((0,0,0))
        conn.send_message(self.socket, b'setname:' + name.encode())
        font = pygame.font.Font(pygame.font.get_default_font(), 18)

        running = True
        while running:
            screen.fill((0,0,0))
            conn.send_message(self.socket, b'read')

            game_state = jsonpickle.decode(conn.receive_message(self.socket))

            players = game_state.players

            if not game_state.is_game_mode:
                text_surface = font.render("Lobby", True, (255,255,255))
                screen.blit(text_surface, dest=(5, 5))
                for i in range(len(players)):
                    text_surface = font.render("- player " + players[i].name, True, (255,255,255))
                    screen.blit(text_surface, dest=(50, 50+i*50))

            else:

                pygame.draw.rect(screen, (255,255,255), (50, 920, 900, 50))

                for i, player in enumerate(filter(lambda p: p.name != name,players)):
                    text_surface = font.render(str(player.name), True, (255,255,255))
                    screen.blit(text_surface, dest=(650, 50 + 75*i))
                    pygame.draw.rect(screen, (255,255,255), (750, 50 + 75*i, 200, 50))
                    for j, card in enumerate(player.hand):
                        #if card["color"] == "Blue":
                        card_text_surface = font.render(card.city_name + "||" + card.color, True, (255, 255, 255))
                        screen.blit(card_text_surface, dest=(50+i*175, 100+j*50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == '__main__':
    ip = 'localhost'
    name = input('enter your name')
    client = Client(ip, name)
