from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from pygame.sprite import Group
from pygame import Rect
import pygame

from client.scene import Scene
from client.ui import MessageBox, Button, Text, InputTextBox

BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)
DARK_GREY = (212, 208, 203)


BULLET_POINT_UNICODE = u'\u2022'


class Chat():

    def __init__(self, initial_state, screen):
        self.players = set([player.name for player in initial_state.players])
        self.group = Group()
        self.screen = screen
        self.messages = []
        self.log_top = 380
        self.scrollbar_height = 330
        self.scrollbar_y = 125
        self.message_offset = 0
        self.chat_window = pygame.Surface((510, 330))

    def add_message(self, msg_text, msg_color=WHITE):
        now = datetime.now()
        timestamp = now.strftime("%I:%M %p")
        msg = "(" + timestamp + ") " + msg_text
        for message in self.messages:
            message.set_xy((message.get_xy()[0], message.get_xy()[1] - 20))
        t = Text(x=300, y=300, size=15, text=msg, color=msg_color, bg=GREY)

        self.group.add(t)
        self.messages.append(t)
        self.log_top = self.messages[0].get_xy()[1]
        if self.log_top < 0:
            total_log_space = -self.log_top + 300
            self.scrollbar_height = (330 / total_log_space) * 330
        else:
            self.scrollbar_height = 330
        self.scrollbar_y = 455 - self.scrollbar_height


    def update(self, server_state, events):
        updated_players = set([player.name for player in server_state.players])
        if updated_players != self.players:
            new_players = updated_players.difference(self.players)
            for player_name in new_players:
                self.add_message(player_name + " joined the lobby.", msg_color=GREEN)

            lost_players = self.players.difference(updated_players)
            for player_name in lost_players:
                self.add_message(player_name + " quit.", msg_color=BLUE)

            self.players = updated_players
        self.group.update(server_state, events)
        print(self.scrollbar_y)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and self.scrollbar_y > 10:
                    self.scrollbar_y -= 10
                elif event.button == 5 and self.scrollbar_y + self.scrollbar_height < 455:
                    self.scrollbar_y += 10

                if self.scrollbar_y < 125:
                    self.scrollbar_y = 125
                if self.scrollbar_y > 455:
                    self.scrollbar_y = 455

                log_height = 330 - self.log_top
                self.message_offset = (1 - ((self.scrollbar_y + self.scrollbar_height ) / 330)) * log_height

                print("log height: " + str(log_height))
                print("scrollbar_y: " + str(self.scrollbar_y))
                print("message offset:" + str(self.message_offset))
        self.chat_window.fill(GREY)
        for message in self.messages:
            self.chat_window.blit(message.image, (0, message.rect.y + self.message_offset))

class Lobby(Scene):
    def __init__(self, screen, channel, chat_channel, initial_state, player_name):
        Scene.__init__(self, screen)

        self.channel = channel
        self.chat_channel = chat_channel
        self.players = []
        self.player_name = player_name

        screen.fill(GREEN)

        self.chat_fetch_executor = ThreadPoolExecutor(max_workers=1)
        self.chat_fetch_future = self.chat_fetch_executor.submit(chat_channel.get_chat_message)

        self.header_group = Group([
            Text(x=50, y=50, size=40, text="Pandemic", bg=DARK_GREY),
            Text(x=50, y=115, size=25, text="Lobby", bg=DARK_GREY)
        ])

        self.button_group = Group(
            Button(x=50, y=470, text="Start game", action=lambda arg: self.channel.request_game_start(), arg=None)
        )

        self.player_names_group = Group(
            [Text(x=50, y=150 + 20 * i, size=15, bg=DARK_GREY, hidden=True) for i in range(4)]
        )

        send_msg_action = lambda msg: self.channel.send_chat_msg(self.player_name, msg)
        self.chat_group = Group(InputTextBox(x=380, y=470, size=20, action=send_msg_action, place_holder="Enter message here"))

        self.groups.append(self.header_group)
        self.groups.append(self.button_group)
        self.groups.append(self.player_names_group)
        self.groups.append(self.chat_group)

        self.chat = Chat(initial_state, screen)

        self.channel.join_lobby(player_name)

    def update(self, server_state, events):
        Scene.update(self, server_state, events)

        self.screen.fill(BLACK)
        self.chat.update(server_state, events)

        if self.chat_fetch_future.done():
            message = chat_msg = self.chat_fetch_future.result()
            self.chat.add_message(message)
            self.chat_fetch_future = self.chat_fetch_executor.submit(self.chat_channel.get_chat_message)

        player_names = list(map(lambda p: p.name, server_state.players))
        for i, name in enumerate(player_names):
            self.player_names_group.sprites()[i].set_hidden(False)
            self.player_names_group.sprites()[i].set_text(BULLET_POINT_UNICODE + " " + name)

        for i in range(3, len(player_names) - 1, -1):
            self.player_names_group.sprites()[i].set_hidden(True)

    def draw(self):
        pygame.draw.rect(self.screen, DARK_GREY, Rect(45, 45, 900, 50))
        pygame.draw.rect(self.screen, DARK_GREY, Rect(45, 110, 300, 400))
        pygame.draw.rect(self.screen, DARK_GREY, Rect(365, 110, 580, 400))
        pygame.draw.rect(self.screen, WHITE, Rect(900, self.chat.scrollbar_y, 30, self.chat.scrollbar_height))
        for message in self.chat.messages:
            self.screen.blit(self.chat.chat_window, (380, 125))
        Scene.draw(self)
