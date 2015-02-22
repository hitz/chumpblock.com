import re
#from enum import Enum
#zones = Enum('hand', 'library', 'graveyard', 'battlefield', 'exile')
zones = ['hand', 'library', 'graveyard', 'battlefield', 'exile']
#permanents = Enum('land', 'creature', 'enchantment', 'artifact', 'planeswalker')
permanents = ['Land', 'Creature', 'Enchantment', 'Artifact', 'Planeswalker']

class Cost(object):
    # does not handle phyrexian, hybrid, or alt casting costs
    # mana costs from MTGJson are {Z} where Z is int or symbol
    # hybrid is {S/T}
    # X is {X}
    # Phyrexian is {Z/P}
    allowed_symbols = ['B', 'G', 'R', 'U', 'W', 'X']
    def __init__(self, fromString="", B=0, G=0, R=0, U=0, W=0, c=0, X=False):
        self.mana = {}
        if fromString:
            bracks = re.compile('[\{\}]')
            syms = bracks.split(fromString)
            for symbol in syms:
                if not symbol:
                    continue
                    # split leaves ""s
                try:
                    colorless = int(symbol)
                    self.mana['colorless'] = colorless
                except ValueError:
                    if symbol == 'X':
                        self.mana['X'] == True
                    elif symbol.find('/') >= 0:
                        print("Cannot parse: %s currently" % (symbol))
                        raise
                    elif symbol in self.allowed_symbols:
                        self.mana[symbol] = self.mana.get(symbol,0) + 1
                    else:
                        print("Unknown mana symbol: %s" % (symbol))
                        raise

        else:
            self.mana['colorless'] = int(c)
            self.mana['B'] = int(B)
            self.mana['G'] = int(G)
            self.mana['R'] = int(R)
            self.mana['U'] = int(U)
            self.mana['W'] = int(W)
            self.mana['X'] = X

    def cmc(self):
        # this could be a one-liner with reduce I am sure
        cmc =0
        for color in self.mana.keys():
            cmc += self.mana[color]


class Card(object):

    def __init__(self, name='', cost='', spells=[], cardData={}):
        if cardData:
            self.name = cardData['name']
            self.mana_cost = Cost(fromString=cardData['manaCost'])
            self.cardData = cardData
            self.is_permanent = False or [ ty for ty in self.cardData['types'] if ty in permanents ]
        else:
            self.name = name
            self.is_permanent = False
            self.mana_cost = Cost(fromString=cost)

        self.spells = spells  # array of functions
        self.zone = 'library'

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
