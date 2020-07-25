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

        self.button_group = Group(Button(50, 50, "Start game"))
        self.player_names_group = Group([
            Text("", 70, 70, 20, hidden=True),
            Text("", 70, 100, 20, hidden=True),
            Text("", 70, 120, 20, hidden=True),
            Text("", 70, 140, 20, hidden=True),
        ])

        self.groups.append(self.button_group)
        self.groups.append(self.player_names_group)

        print("sending msg about joinin the lobby")

        self.channel.join_lobby(player_name)

        print("lobby initialized")

    def update(self, server_state):
        self.screen.fill(BLACK)
        Scene.update(self, server_state)

        print("updating lobby")

        player_names = list(map(lambda p: p.name, server_state.players))
        for i, name in enumerate(player_names):
            self.player_names_group.sprites()[i].set_hidden(False)
            self.player_names_group.sprites()[i].set_text(name)

        print(player_names)
        print(list(range(3, len(player_names) - 1, -1)))
        for i in range(3, len(player_names) - 1, -1):
            self.player_names_group.sprites()[i].set_hidden(True)
