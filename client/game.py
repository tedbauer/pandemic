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
from client.ui import WHITE

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


    def draw_edges(self, root_node, surface, visited):
        if root_node.city_name in visited:
            return

        visited.add(root_node.city_name)

        for neighbor in root_node.neighbors:
            root_pos = root_node.rect.x + self.x, root_node.rect.y + self.y
            neighbor_pos = neighbor.rect.x + self.x, neighbor.rect.y + self.y
            pygame.draw.line(surface, WHITE, root_pos, neighbor_pos)
            self.draw_edges(neighbor, surface, visited)


    def draw(self, surface):
        # TODO(ted): the overridden draw() might have useful functionality that we're missing
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x + self.x, sprite.rect.y + self.y))

        # TODO(ted): disentangle CameraGroup and this edge logic
        visited = set()
        self.draw_edges(next(s for s in self.sprites() if s.city_name == "Chicago"), surface, visited)

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

    def create_city_sprites(self, city_nodes):
        sprite_map = dict()
        city_group = CameraGroup()

        for city_node in city_nodes:
            x, y = random.randint(0, 600), random.randint(0, 600)
            city_sprite = City(x, y, color_map[city_node.color.lower()], city_node.city_name, [])
            city_group.add(city_sprite)
            sprite_map[city_node.city_name] = city_sprite

        for city_node in city_nodes:
            for neighbor in city_node.neighbors:
                neighbor_sprite = sprite_map[neighbor.city_name]
                sprite_map[city_node.city_name].neighbors.append(neighbor_sprite)

        return city_group


    def __init__(self, screen, channel, initial_state):
        Scene.__init__(self, screen)

        self.screen = screen
        self.channel = channel

        self.groups.append(self.create_city_sprites(initial_state.city_nodes))


    def update(self, server_state, events):
        self.screen.fill((0, 0, 0))
        Scene.update(self, server_state, events)
