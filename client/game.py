import random

import pygame
from pygame.sprite import Group

from client.board import City
from client.scene import Scene

from client.ui import BLUE
from client.ui import YELLOW
from client.ui import GREEN
from client.ui import BLACK

color_map = {
    "blue": BLUE,
    "yellow": YELLOW,
    "green": GREEN,
    "black": BLACK,
}

class Game(Scene):

    def __init__(self, screen, channel, initial_state):
        Scene.__init__(self, screen)

        self.screen = screen
        self.channel = channel

        city_group = Group()
        for city_node in initial_state.city_nodes:
            x, y = random.randint(0, 600), random.randint(0, 600)
            city_group.add(City(x, y, color_map[city_node.color.lower()], city_node.city_name, None))

        self.groups.append(city_group)


    def update(self, server_state, events):
        self.screen.fill((0, 0, 0))
        Scene.update(self, server_state, events)
