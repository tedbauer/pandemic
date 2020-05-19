import conn
import socket
import pygame
import jsonpickle

BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

class Client:

    def __init__(self, ip, name):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, 1066))

        pygame.init()
        screen = pygame.display.set_mode((1000, 800))
        screen.fill((20,20,20))
        conn.send_message(self.socket, b'setname:' + name.encode())
        font = pygame.font.Font(pygame.font.get_default_font(), 10)

        running = True
        while running:
            screen.fill((20,20,20))
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

                pygame.draw.rect(screen, (255,255,255), (100, 650, 700, 100))
                my_hand = next(p for p in players if p.name == name).hand
                for i, card in enumerate(my_hand):
                    if card.color == "Blue":
                        color = BLUE
                    elif card.color == "Yellow":
                        color = YELLOW
                    elif card.color == "Green":
                        color = GREEN
                    else:
                        color = BLACK
                    pygame.draw.rect(screen, color, (110 + 90 * i, 660, 80, 80))
                    my_card_text_surface = font.render(card.city_name, True, WHITE)
                    screen.blit(my_card_text_surface, dest=(110 + 90*i, 660))

                for i, player in enumerate(filter(lambda p: p.name != name,players)):
                    text_surface = font.render(str(player.name), True, (255,255,255))
                    screen.blit(text_surface, dest=(550, 70 + 120*i))
                    pygame.draw.rect(screen, (255,255,255), (600, 50 + 120*i, 400, 100))
                    for j, card in enumerate(player.hand):
                        if card.color == "Blue":
                            color = BLUE
                        elif card.color == "Yellow":
                            color = YELLOW
                        elif card.color == "Green":
                            color = GREEN
                        else:
                            color = BLACK
                        pygame.draw.rect(screen, color, (620 + 90 * j, 60 + 120*i, 80, 80))
                        card_text_surface = font.render(card.city_name, True, (100, 100, 100))
                        screen.blit(card_text_surface, dest=(620 + 90 * j, 60 + 120*i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == '__main__':
    ip = 'localhost'
    name = input('enter your name')
    client = Client(ip, name)
