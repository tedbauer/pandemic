import random

import pygame
from pygame.sprite import Group
from pygame import Rect

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

class CameraGroup(Group):

    def __init__(self):
        Group.__init__(self)
        self.x = 0
        self.y = 0

        self.upper_box = Rect(0, 0, 1000, 150)
        self.lower_box = Rect(0, 650, 1000, 150)
        self.left_box = Rect(0, 0, 150, 800)
        self.right_box = Rect(850, 0, 150, 800)
        self.camera_speed = 5


    def draw(self, surface):
        #TODO: the overridden draw() might have useful functionality that we're missing
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x + self.x, sprite.rect.y + self.y))


    def update(self, server_state, events):
        Group.update(self, server_state, events)

        if self.upper_box.collidepoint(pygame.mouse.get_pos()):
            self.y -= self.camera_speed
        if self.lower_box.collidepoint(pygame.mouse.get_pos()):
            self.y += self.camera_speed
        if self.left_box.collidepoint(pygame.mouse.get_pos()):
            self.x -= self.camera_speed
        if self.right_box.collidepoint(pygame.mouse.get_pos()):
            self.x += self.camera_speed


class Game(Scene):

    def __init__(self, screen, channel, initial_state):
        Scene.__init__(self, screen)

        self.screen = screen
        self.channel = channel

        city_group = CameraGroup()
        for city_node in initial_state.city_nodes:
            x, y = random.randint(0, 600), random.randint(0, 600)
            city_group.add(City(x, y, color_map[city_node.color.lower()], city_node.city_name, None))

        self.groups.append(city_group)


    def update(self, server_state, events):
        self.screen.fill((0, 0, 0))
        Scene.update(self, server_state, events)
