import pygame

class Scene:
    def __init__(self, screen):
        self.groups = []
        self.screen = screen

    def update(self, server_state, events):
        for group in self.groups: group.update(server_state, events)

    def draw(self):
        for group in self.groups:
            group.draw(self.screen)
        pygame.display.flip()


