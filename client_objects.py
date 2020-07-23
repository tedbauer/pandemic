from pygame.sprite import Sprite
import pygame

class City(Sprite):
    def __init__(self, x, y, color, neighbors):
        super()

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (x, y), 50)
        self.rect = self.image.get_rect()

        self.neighbors = neighbors

    def update(self):
        pass
