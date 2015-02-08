#import pytest

from cards import cards as cards

data = [
        { '2G': {
            'colorless': 2,
            'G': 1
            }
        },
        { '3BB': {
            'colorless': 3,
            'B': 2
            }
        },
        { 'U': {
            'U': 1
            }
        },
        { 'GWR': {
            'G': 1,
            'W': 1,
            'R': 1
            }
        },
        { '4': {
            'colorless': 4,
            }
        },
        { '2GGWWUU': {
            'colorless': 2,
            'G': 2,
            'W': 2,
            'U': 2
            }
        }
]

def test_cards():

    for sample in data:
        for cost_str in sample.keys():
            cost = cards.Cost(fromString=cost_str)
            assert cost.mana == sample[cost_str]

    print "%s tests passed" % len(data)

if __name__ == '__main__':
    test_cards()

