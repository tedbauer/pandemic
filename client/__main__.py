from concurrent.futures import ThreadPoolExecutor

import pygame

from client.chat_channel import ChatChannel
from client.server_channel import ServerChannel
from client.lobby import Lobby
from client.game import Game

if __name__ == '__main__':
    ip = 'localhost'
    name = input('enter your name: ')

    pygame.init()
    pygame.display.set_caption("Pandemic")

    screen = pygame.display.set_mode((1000, 800))
    channel = ServerChannel(ip, 1066)
    chat_channel = ChatChannel(ip, 1099)

    server_state = channel.read_new_state()

    scene = Lobby(screen, channel, chat_channel, server_state, name)
    game_started = False

    state_fetch_executor = ThreadPoolExecutor(max_workers=1)
    state_fetch_future = state_fetch_executor.submit(channel.read_new_state)

    running = True
    while running:
        if state_fetch_future.done():
            server_state = state_fetch_future.result()
            state_fetch_future = state_fetch_executor.submit(channel.read_new_state)

        if server_state.is_game_mode and not game_started:
            scene = Game(screen, channel, server_state)
            game_started = True

        events = pygame.event.get()
        scene.update(server_state, events)
        scene.draw()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

