from pygame.sprite import Sprite, OrderedUpdates
from pygame import Rect
import pygame

BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)

class WindowRectangle(Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class Text(Sprite):
    def __init__(self, x=100, y=100, size=20, text="", bold=False, hidden=False):
        super().__init__()

        self.text = text
        self.hidden = hidden

        self.font = pygame.font.Font(pygame.font.get_default_font(), size)
        self.text_surface = self.font.render(text, 1, WHITE)

        self.image = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)

        if not hidden: self.image.blit(self.text_surface, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.new_text = None

    def set_text(self, new_text):
        self.new_text = new_text

    def set_hidden(self, new_hidden):
        self.hidden = new_hidden

    def update(self, s, events):
        if self.new_text:
            self.text = self.new_text
            self.text_surface = self.font.render(self.text, 1, WHITE)
            self.image = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)
            self.new_text = None

        # TODO: only blit/fill if needed
        if self.hidden:
            self.image.fill(BLACK)
        else:
            self.image.fill(BLACK)
            self.text_surface = self.font.render(self.text, 1, WHITE)
            self.image.blit(self.text_surface, (0, 0))


class Button(Sprite):
    def __init__(self, x=50, y=50, text="", action=lambda arg: None, arg=None):
        super().__init__()

        self.action = action
        self.arg = arg
        self.color = GREY

        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.text_surface = self.font.render(text, 1, WHITE)

        text_width, text_height = self.text_surface.get_size()
        self.image = pygame.Surface((text_width+5, text_height+5))
        self.image.fill(self.color)
        self.image.blit(self.text_surface, (2.5, 2.5))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def update(self, s, events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = GREEN
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.action(self.arg)
        else:
            self.color = GREY
        self.image.fill(self.color)
        self.image.blit(self.text_surface, (2.5, 2.5))

class MessageBox(OrderedUpdates):
    def __init__(self, x, y, title, items, button_text):
        super().__init__()

        self.x = x
        self.y = y
        self.text_items = []
        for i, item in enumerate(items):
            color = GREY if i % 2 == 0 else GREEN
            self.add(WindowRectangle(color, x, y+50+30*i, 300, 20))
            self.add(Text(item, x+5, y+50+30*i+1, 20))
            self.text_items.append(WindowRectangle(color, x, y+50+30*i, 300, 20))
            self.text_items.append(Text(item, x+5, y+50+30*i+1, 20))

        self.add(WindowRectangle(BLACK, x, y, 300, 400))
        self.add(Button(x+5, y+365, button_text))
        self.add(Text(title, x+5, y+5, 32, bold=True))

    def set_items(self, items):
        for item in self.text_items: item.kill()
        for i, item in enumerate(items):
            color = GREY if i % 2 == 0 else GREEN
            x, y = self.x, self.y
            self.add(WindowRectangle(color, x, y+50+30*i, 300, 20))
            self.add(Text(item, x+5, y+50+30*i+1, 20))
            self.text_items.append(WindowRectangle(color, x, y+50+30*i, 300, 20))
            self.text_items.append(Text(item, x+5, y+50+30*i+1, 20))
