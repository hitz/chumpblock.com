import random
import json
import cards

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

    def load_deck(self, input_file=''):
        df = open(input_file)


class CardDB(object):
    def __init__(self, input_file='data/AllSets-x.json'):
        self.all = json.load(open(input_file))

        hashed = {}
        for s in self.all.values():
            hashed.update({ c['name']: c for c in s['cards'] })

        self.by_card = hashed



