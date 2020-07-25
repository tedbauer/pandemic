from concurrent.futures import ThreadPoolExecutor

import pygame
from pygame.sprite import Group

from client.server_channel import ServerChannel
from client.ui import MessageBox, Button


BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
NODEPOSITIONS   = dict()

class Scene:
    def __init__(self, screen):
        self.groups = []
        self.screen = screen

    def update(self, server_state):
        for group in self.groups: group.update(server_state)

    def draw(self):
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()


class Lobby(Scene):
    def __init__(self, screen, channel, player_name):
        Scene.__init__(self, screen)

        self.channel = channel
        self.players = []

        screen.fill(BLACK)

        button_group = Group(Button(50, 50, "Start game"))
        self.groups.append(button_group)

        self.channel.join_lobby(player_name)

    def update(self, server_state):
        self.screen.fill(BLACK)
        Scene.update(self, server_state)

        self.players = list(map(lambda p: p.name, server_state.players))
        print(self.players)


class Client:
    def __init__(self, ip, name):

        pygame.init()

        screen = pygame.display.set_mode((1000, 800))
        self.channel = ServerChannel(ip, 1066)
        self.scene = Lobby(screen, self.channel, name)

        server_state = self.channel.read_new_state()

        state_fetch_executor = ThreadPoolExecutor(max_workers=1)
        state_fetch_future = state_fetch_executor.submit(self.channel.read_new_state)

        running = True
        while running:
            if state_fetch_future.done():
                server_state = state_fetch_future.result()
                state_fetch_future = state_fetch_executor.submit(self.channel.read_new_state)

            self.scene.update(server_state)
            self.scene.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == '__main__':
    ip = 'localhost'
    name = input('enter your name: ')
    client = Client(ip, name)
