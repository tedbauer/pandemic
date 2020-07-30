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

class InputTextBox(Sprite):
    def __init__(self, x=100, y=100, size=20, place_holder="", action=lambda x:None, bg=BLACK):
        super().__init__()

        self.place_holder = place_holder
        self.text = ""
        self.action = action
        self.active = False
        self.bg = bg

        self.font = pygame.font.Font(pygame.font.get_default_font(), size)
        self.text_surface = self.font.render(self.text, 1, bg)

        self.image = pygame.Surface((510, 25), pygame.SRCALPHA)

        self.image.blit(self.text_surface, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def update(self, s, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.text = self.text[:-1]
        else:
            for event in events:
                if event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        self.action(self.text)
                        self.text = ""
                    else:
                        self.text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.active = True
                    else:
                        self.active = False

        self.image.fill(WHITE)
        if self.active:
            self.text_surface = self.font.render(self.text, 1, self.bg)
        else:
            self.text_surface = self.font.render(self.place_holder, 1, GREY)
        self.image.blit(self.text_surface, (0, 0))


class Text(Sprite):
    def __init__(self, x=100, y=100, size=20, text="", bold=False, hidden=False, color=WHITE, bg=BLACK):
        super().__init__()

        self.text = text
        self.hidden = hidden
        self.color = color
        self.bg = bg

        self.font = pygame.font.Font(pygame.font.get_default_font(), size)
        self.text_surface = self.font.render(text, 1, self.color)

        self.image = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)

        if not hidden: self.image.blit(self.text_surface, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.new_text = None

    def get_xy(self):
        return self.rect.topleft

    def set_xy(self, xy):
        self.rect.topleft = xy

    def set_text(self, new_text):
        self.new_text = new_text

    def set_hidden(self, new_hidden):
        self.hidden = new_hidden

    def update(self, s, events):
        if self.new_text:
            self.text = self.new_text
            self.text_surface = self.font.render(self.text, 1, self.color)
            self.image = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)
            self.new_text = None

        # TODO: only blit/fill if needed
        if self.hidden:
            self.image.fill(self.bg)
        else:
            self.image.fill(self.bg)
            self.text_surface = self.font.render(self.text, 1, self.color)
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
