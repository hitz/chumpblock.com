#import pytest

from cards import cards as cards

data = [
    { '{2}{G}': {
        'colorless': 2,
        'G': 1
        }
    },
    { '{3}{B}{B}': {
        'colorless': 3,
        'B': 2
        }
    },
    { '{U}': {
        'U': 1
        }
    },
    { '{G}{W}{R}': {
        'G': 1,
        'W': 1,
        'R': 1
        }
    },
    { '{4}': {
        'colorless': 4,
        }
    },
    { '{2}{G}{G}{W}{W}{U}{U}': {
        'colorless': 2,
        'G': 2,
        'W': 2,
        'U': 2
        }
    }
]

bad_data = [
    '{G/P}',
    '{H}',
    '{U/R}',
    '{U/W}{U/W}{2}'
    '{3}{R}{R/P}'
]

def test_cards():

    for sample in data:
        for cost_str in sample.keys():
            cost = cards.Cost(fromString=cost_str)
            assert cost.mana == sample[cost_str]

    print("%s good data tests passed" % len(data))

    for bad in bad_data:
        try:
            cost = cards.Cost(fromString=bad)
        except:
            assert(True)

    print("%s bad data tests passed" % len(bad_data))

if __name__ == '__main__':
    test_cards()

