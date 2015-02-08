import re
from enum import Enum
zones = Enum('hand', 'library', 'graveyard', 'battlefield', 'exile')
permanents = Enum('land', 'creature', 'enchantment', 'artifact', 'planeswalker')

class Cost(object):
    # does not handle phyrexian, hybrid, X, or alt casting costs
    symbols = ['B', 'G', 'R', 'U', 'W']
    def __init__(self, fromString="", B=0, G=0, R=0, U=0, W=0, c=0):
        self.mana = {}
        if fromString:
            colorless = re.search(r"(\d+)", fromString)
            if colorless:
                self.mana['colorless'] = int(colorless.group(0))

            for color in self.symbols:
                ss = '('+color+')+'
                found = re.search(ss, fromString)
                if found:
                    self.mana[color] = len(found.group(0))
        else:
            self.mana['colorless'] = int(c)
            self.mana['B'] = int(B)
            self.mana['G'] = int(G)
            self.mana['R'] = int(R)
            self.mana['U'] = int(U)
            self.mana['W'] = int(W)

    def cmc(self):
        # this could be a one-liner with reduce I am sure
        cmc =0
        for color in self.mana.keys():
            cmc += self.mana[color]


class Card(object):

    def __init__(self, name, cost, spells):
        self.name = name
        self.is_permanent = False
        self.zone = 'library'
        self.mana_cost = Cost(fromString=cost)
        self.spells = spells  # array of functions

    def draw(self):
        self.zone = 'hand'

    def destroy(self):
        self.zone = 'graveyard'

    def exile(self):
        self.zone = 'exile'

    def play(self, context):

        self.pay_cost(context)  # need some sort of game context object
        self.zone = 'battlefield'


class PermanentMixin(object):
    def __init__(self):
        self.is_permanent = True


class ArtifactMixin(object):
    def __init__(self):
        self.is_artifact = True


class LegendaryMixin(object):
    def __init__(self):
        self.is_legendary = True

    def play(self, context):
        others = context.battlefield.get(self.name)
        if not others:
            super(Card, LegendaryMixin).play()
        else:
            self.destroy()
            [o.destroy() for o in others]


class Creature(Card, PermanentMixin):

    def __init__(self, name, cost, spells, power, toughness, type, subtypes):
        super(Card, Creature).__init__(name, cost, spells)
        self.type = 'creature'
        self.power = power
        self.toughness = toughness
        self.damage = 0
        self.subtypes = subtypes


class Enchantment(Card, PermanentMixin):
    def __init__(self, name, cost, spells, target_type):
        super(Card, Enchantment).__init__(name, cost, spells)
        self.type = 'enchantment'
        self.target_type = target_type
