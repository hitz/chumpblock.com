import sys
import os
import decks
import players

DECKS_DIR = 'data/decks/'

def run(turns, rounds, decks, goldfish=True):
    print("Running %s games for %s turns...") % (rounds, turns)
    if goldfish:
        print("In goldfish (single player) mode")
        nplayers = 1
    else:
        nplayers = 2
        print("Can only goldfish, sorry")
        sys.exit(1)

    ourplayers = []
    for round in range(0,rounds):
        print("Round %s... FIGHT" % (round+1))
        for n in range(0,nplayers):
            player = players.Player(name="Player%s" % n, deck=deck)
            player.mulligan(rules={})
            print("After mulligans player %s has %s cards [%s]" % (player.name, len(player.hand), player.hand))
            ourplayers.append(player)





def main():
    import argparse
    parser = argparse.ArgumentParser(description='Magic game sim')
    parser.add_argument('--turns', type=int, metavar='T', help="Number of turns each sim game runs", default=20)
    parser.add_argument('--rounds', type=int, metavar='N', help="Number of sim games", default=1)
    parser.add_argument('--decks', metavar='D', help='Decks to play', nargs='+')
    #parser.add_argument('updatefile', type=argparse.FileType('wb'))
    args = parser.parse_args()

    decks = []
    for deck_file in args.decks:
        d = decks.Deck()
        try:
            os.stat(deck_file)
            d.load_deck(deck_file)
        except OSError:
            try:
                os.stat(DECKS_DIR+deck_file)
                d.load_deck(DECKS_DIR+deck_file)
            except OSError:
                print("Could not find %s to load" % deck_file)

        decks.append(d)

    if len(decks) < 1 or len(decks) > 2:
        print("Please supply 1 or 2 decks instead of %s" % (len(decks)))


    run(args.turns, decks, args.rounds)

if __name__ == '__main__':
    main()
else:
    print "Foo"