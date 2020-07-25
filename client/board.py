from pygame.sprite import Sprite
import pygame

class City(Sprite):
    def __init__(self, x, y, color, city_name, neighbors):
        super().__init__()

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (25, 25), 12)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.city_name = city_name
        self.color = color
        self.neighbors = neighbors
