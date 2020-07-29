from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from pygame.sprite import Group

from client.scene import Scene
from client.ui import MessageBox, Button, Text, InputTextBox

BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

BULLET_POINT_UNICODE = u'\u2022'


class Chat():

    def __init__(self, initial_state, screen):
        self.players = set([player.name for player in initial_state.players])
        self.group = Group()
        self.screen = screen
        self.messages = []

    def add_message(self, msg_text, msg_color=WHITE):
        now = datetime.now()
        timestamp = now.strftime("%I:%M %p")
        msg = "(" + timestamp + ") " + msg_text
        for message in self.messages:
            message.set_xy((message.get_xy()[0], message.get_xy()[1] - 50))
        t = Text(x=300, y=300, size=25, text=msg, color=msg_color)
        self.group.add(t)
        self.messages.append(t)


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
            Text(x=50, y=50, size=40, text="Pandemic"),
            Text(x=50, y=100, size=25, text="Lobby")
        ])

        self.button_group = Group(
            Button(x=50, y=210, text="Start game", action=lambda arg: self.channel.request_game_start(), arg=None)
        )

        self.player_names_group = Group(
            [Text(x=50, y=130 + 20 * i, size=15, hidden=True) for i in range(4)]
        )

        send_msg_action = lambda msg: self.channel.send_chat_msg(self.player_name, msg)
        self.chat_group = Group(InputTextBox(x=300, y=350, size=20, action=send_msg_action, place_holder="Enter message here"))

        self.groups.append(self.header_group)
        self.groups.append(self.button_group)
        self.groups.append(self.player_names_group)
        self.groups.append(self.chat_group)

        self.chat = Chat(initial_state, screen)
        self.groups.append(self.chat.group)

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
