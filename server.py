import random
import csv
import socket

# deal cards to beginning players
# 2-4 players; each player gets a deck of cards

class Card:
    def __init__(self, city_name, color):
        self.color = color
        self.city_name = city_name

class Deck:
    def __init__(self):
        with open("assets/CityCard_Types.csv", newline="") as city_color_file:
            reader = csv.reader(city_color_file, delimiter=",")
            next(reader)
            self.deck = [Card(row[0], row[1]) for row in reader]

    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

class GameState:
    def __init__(self, players):
        self.players = players # list of Player objects
        self.deck = Deck()

        if len(players) == 2:
            for player in players:
                for _ in range(4): player.hand.append(self.deck.draw_card())
        elif len(players) == 3:
            for player in players:
                for _ in range(3): player.hand.append(self.deck.draw_card())
        elif len(players) == 4:
            for player in players:
                for _ in range(2): player.hand.append(self.deck.draw_card())

class Server:
    def __init__(self):
        port = 1066  # assigned randomly, any number of 1032
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # opening a TCP connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))  # telling the socket to use our host and port that we specified
        s.listen(1)  # only allowing one connection
        print("listening on port " + str(port))
        conn, addr = s.accept()
        print("Connection formed" + str(conn))
        while True:
            data = conn.recv(1024)  # getting data from the connection; getting in chunks of 1024 max; loops to get more data
            if not data: break
            print("msg from client: " + str(data))
            conn.sendall(data)
        conn.close()
