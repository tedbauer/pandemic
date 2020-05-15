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
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

class Server:
    def __init__(self):
        host = socket.gethostbyname(socket.gethostname())  # returns MY IP address
        port = 1066  # assigned randomly, any number of 1032
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # opening a TCP connection
        s.bind((host, port))  # telling the socket to use our host and port that we specified
        s.listen(1)  # only allowing one connection
        print(host + " listening on port " + str(port))
        conn, addr = s.accept()
        print("Connection formed" + conn)
        while True:
            data = conn.recv(1024)  # getting data from the connection; getting in chunks of 1024 max; loops to get more data
            if not data: break
            conn.sendall(data)
        conn.close()



s = Server()