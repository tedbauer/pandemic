import random
# deal cards to beginning players
# 2-4 players; each player gets a deck of cards

class Card:
    def __init__(self, color, city_name):
        self.color = color
        self.city_name = city_name

class Deck:
    def __init__(self):
        self.cards = [Card("blue", "Chennai"), Card("yellow", "San Francisco"), Card("black", "London")]
        # pick a random number to establish deck order
        # e.g. a list of randomly scrambled non repeating numbers
        self.deck_order = []
        for i in range(48):
            num = random.randint(0,48)
            while num in self.deck_order:
                num = random.randint(0,48)
            self.deck_order.append(num)

d = Deck()
print(d.deck_order)