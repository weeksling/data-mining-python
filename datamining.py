
import sys, argparse
import time

from aprioriv2 import apriori
from pcy import pcy

APRIORI = 'APRIORI'
PCY = 'PCY'

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alg", default=APRIORI, choices=[APRIORI, PCY],
        help="Name of algorithm to be used. Options: 'PCY' or 'APRIORI'. Default: 'APRIORI'")
    parser.add_argument("-s", "--support", default=0.03, type=float, 
        help="The minimum %% of buckets a candidate must be in to be accepted (ex: 0.03)")
    parser.add_argument("datafile", type=file, help="The name of the file to be mined for data")
    args = parser.parse_args()

    return args.datafile, args.alg, args.support


def main():
    datafile, algorithm, minSupport = get_options()
    start = time.time()

    if (algorithm == APRIORI):
        results = apriori(datafile, minSupport)
    elif (algorithm == PCY):
        results = pcy(datafile, minSupport)

    print results
    print 'elapsed', time.time() - start
    return results

if __name__ == "__main__":
   main()