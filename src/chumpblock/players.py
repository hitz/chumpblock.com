import random

class Player(object):

    def __init__(self, name='Default1', deck=None, life=20, poison=10):
        self.name = name
        self.deck = deck
        self.life = life
        self.poison = poison
        self.hand = []
        self.graveyard = []
        self.exile = []

        self.battlefield = []


    def _satisfied(self, rules, n):
        if not rules:
            if len(self.hand) and len(self.hand) < 5:
                # keep all 4s
                return True
            elif len([ c for c in self.hand if c.isLand() ]) and len([ c for c in self.hand if not c.isLand() ]):
                    return True
            else:
                return False

    def mulligan(self, rules={}, n=7):
        ''' draw an initial hand and paris mulligan until acceptable by rules
            default rules are mulligan 0 land and 0 non-land hands until 4, then keep '''

        self.deck.shuffle()
        self.hand = []
        if n==7:
            print("Drawing initial 7...")
        else:
            print("Mulling to %s...") % (n)
        for i in range(0,n):
            self.hand.append(self.deck.drawCard())

        while(not self._satisfied(rules, n)):
            self.mulligan(rules,n-1)

        print("Final hand %s" % (self.hand))
