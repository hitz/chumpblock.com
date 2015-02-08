import random

class Deck(object):

    def __init__(self):
        self.order = []
        return self

    def shuffle(self):
        random.shuffle(self.order)

    def drawCard(self):
        return self.order.pop()

    def putOnTop(self, card):
        self.order.append(card)

    def putOnBottom(self, card):
        self.order.insert(0,card)
