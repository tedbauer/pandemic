from pygame.sprite import Group

from client.scene import Scene
from client.ui import MessageBox, Button, Text

BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

BULLET_POINT_UNICODE = u'\u2022'



class Lobby(Scene):
    def __init__(self, screen, channel, player_name):
        Scene.__init__(self, screen)

        self.channel = channel
        self.players = []

        screen.fill(GREEN)

        self.header_group = Group([
            Text(50, 50, 40, text="Pandemic"),
            Text(50, 100, 25, text="Lobby")
        ])

        self.button_group = Group(
            Button(x=50, y=210, text="Start game", action=lambda arg: self.channel.request_game_start(), arg=None)
        )

        self.player_names_group = Group(
            [Text(x=50, y=130 + 20 * i, size=15, hidden=True) for i in range(4)]
        )

        self.groups.append(self.header_group)
        self.groups.append(self.button_group)
        self.groups.append(self.player_names_group)

        self.channel.join_lobby(player_name)

    def update(self, server_state, events):
        Scene.update(self, server_state, events)

        self.screen.fill(BLACK)

        player_names = list(map(lambda p: p.name, server_state.players))
        for i, name in enumerate(player_names):
            self.player_names_group.sprites()[i].set_hidden(False)
            self.player_names_group.sprites()[i].set_text(BULLET_POINT_UNICODE + " " + name)

        for i in range(3, len(player_names) - 1, -1):
            self.player_names_group.sprites()[i].set_hidden(True)
