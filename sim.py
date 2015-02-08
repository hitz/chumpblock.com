def run(turns, rounds):
    print "Running %s games for %s turns..." % (rounds, turns)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Magic game sim')
    parser.add_argument('turns', type=int, metavar='T', help="Number of turns each sim game runs")
    parser.add_argument('rounds', type=int, metavar='N', help="Number of sim games")
    #parser.add_argument('updatefile', type=argparse.FileType('wb'))
    args = parser.parse_args()
    run(args.turns, args.rounds)
    #args.infile.close()
    #args.infile = open(args.infile.name, 'rb')

if __name__ == '__main__':
    main()
else:
    print "Foo"