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

    def create_cities(self, root_city, city_group, visited_acc):
        if root_city in visited_acc:
            return

        x, y = random.randint(0, 600), random.randint(0, 600)
        city_group.add(City(x, y, color_map[root_city.color.lower()], root_city.city_name, None))
        visited_acc.add(root_city.city_name)

        for neighbor in root_city.neighbors:
            create_cities(neighbor, city_group, visited_acc)


    def __init__(self, screen, channel, initial_state):
        Scene.__init__(self, screen)

        self.screen = screen
        self.channel = channel

        city_group = Group()
        visited = set()
        print("init was called")
        self.create_cities(initial_state.city_nodes[0], city_group, visited)

        self.groups.append(city_group)


    def update(self, server_state, events):
        self.screen.fill((0, 0, 0))
        Scene.update(self, server_state, events)
