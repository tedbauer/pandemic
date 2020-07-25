from concurrent.futures import ThreadPoolExecutor

import pygame

from client.server_channel import ServerChannel
from client.lobby import Lobby

if __name__ == '__main__':
    ip = 'localhost'
    name = input('enter your name: ')

    pygame.init()


    screen = pygame.display.set_mode((1000, 800))
    channel = ServerChannel(ip, 1066)


    print("initialized server channel")
    scene = Lobby(screen, channel, name)

    print("initialized lobby")

    server_state = channel.read_new_state()

    state_fetch_executor = ThreadPoolExecutor(max_workers=1)
    state_fetch_future = state_fetch_executor.submit(channel.read_new_state)

    print("here now...")

    running = True
    while running:
        if state_fetch_future.done():
            server_state = state_fetch_future.result()
            state_fetch_future = state_fetch_executor.submit(channel.read_new_state)

        print("here now")

        scene.update(server_state)
        scene.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

