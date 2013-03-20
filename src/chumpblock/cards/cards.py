zones = ['hand', 'library', 'graveyard', 'battlefield', 'exile']


class Card(object):

    def __init__(self, name, cost, spells):
        self.name = name
        self.is_permanent = False
        self.zone = 'library'
        self.mana_cost = cost or {
            'B': 0,
            'U': 0,
            'G': 0,
            'R': 0,
            'C': 0,
            'hybrid': {},
        }
        self.spells = spells  # array of functions

    def draw(self):
        self.zone = 'hand'

    def destroy(self):
        self.zone = 'graveyard'

    def exile(self):
        self.zone = 'exile'

    def play(self):

        self.pay_cost()  # need some sort of game context object
        self.zone = 'battlefield'


class PermanentMixin(Object):
    def __init__(self):
        self.is_permanent = True


class ArtifactMixin(Objeect):
    def __init__(self):
        self.is_artifact = True


class LegendaryMixin(Object):
    def __init__(self):
        self.is_legendary = True


    def play(self:
        others = context.battlefield.get(self.name)
        if not others:
            __super__.play()
        else:
            self.destroy()
            [o.destroy() for o in others]


class Creature(Card, PermanentMixin):

    def __init__(self, name, cost, spells, power, toughness, type, subtypes):
        __super__.__init__(name, cost, spells)
        self.type = 'creature'
        self.power = power
        self.toughness = toughness
        self.damage = 0
        self.subtypes = subtypes

class Enchantmente(Card, PermanentMixin):
