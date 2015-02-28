import re
#from enum import Enum
#zones = Enum('hand', 'library', 'graveyard', 'battlefield', 'exile')
zones = ['hand', 'library', 'graveyard', 'battlefield', 'exile']
#permanents = Enum('land', 'creature', 'enchantment', 'artifact', 'planeswalker')
permanents = ['Land', 'Creature', 'Enchantment', 'Artifact', 'Planeswalker']

class Cost(object):
    # does not handle phyrexian, or alt casting costs
    # mana costs from MTGJson are {Z} where Z is int or symbol
    # hybrid is {S/T}
    # X is {X}
    # Phyrexian is {Z/P}
    base_symbols = ['B', 'G', 'R', 'U', 'W']
    allowed_symbols = base_symbols+['X']
    for a in base_symbols:
        allowed_symbols.append(a+'/P')
        for b in base_symbols[1:]:
            if a==b:
                continue
            else:
                allowed_symbols.append(a+'/'+b)
                allowed_symbols.append(b+'/'+a)

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
                    elif symbol in self.allowed_symbols:
                        self.mana[symbol] = self.mana.get(symbol,0) + 1
                    else:
                        print("Unknown mana symbol: %s" % (symbol))
                        raise

        else:
            ## warning does not handle hybrid/phyrexian use fromString!!!
            self.mana['colorless'] = int(c)
            self.mana['B'] = int(B)
            self.mana['G'] = int(G)
            self.mana['R'] = int(R)
            self.mana['U'] = int(U)
            self.mana['W'] = int(W)
            self.mana['X'] = X

    def cmc(self):
        return self.cardData.get('cmc',0)

    def __str__(self):
        return "[ %s (%s) ]" % (self.name, self.cardData.get('manaCost', '0'))


class Card(object):

    def __init__(self, name='', cost='', spells=[], cardData={}):
        if cardData:
            self.name = cardData['name']
            self.mana_cost = Cost(fromString=cardData.get('manaCost',''))
            self.cardData = cardData
        else:
            self.name = name
            self.mana_cost = Cost(fromString=cost)

        self.spells = spells  # array of functions
        self.zone = 'library'

    def isLand(self):
        return 'Land' in self.cardData['types']

    def isPermanent(self):
        return False or bool([ ty for ty in self.cardData['types'] if ty in permanents ])

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
        # this is the old Legendary rule
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
