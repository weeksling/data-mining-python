
import sys, argparse
import time

from apriori import apriori
from pcy import pcy

APRIORI = 'APRIORI'
PCY = 'PCY'

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alg", default=APRIORI, choices=[APRIORI, PCY],
        help="Name of algorithm to be used. Options: 'PCY' or 'APRIORI'. Default: 'APRIORI'")
    parser.add_argument("-s", "--support", default=0.03, type=float, 
        help="The minimum %% of itemsets a candidate must be in to be accepted (ex: 0.03)")
    parser.add_argument("-b", "--buckets", default=500, type=int,
        help="The number of buckets that will be used in PCY algorithm. Default: 500")
    parser.add_argument("datafile", type=file, help="The name of the file to be mined for data")
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-t", action="store_true")
    args = parser.parse_args()

    return args.datafile, args.alg, args.support, args.buckets, args.v, args.t

def mine_data(algorithm, datafile, minSupport, num_buckets, is_verbose):
    if (algorithm == APRIORI):
        return apriori(datafile, minSupport, v=is_verbose)
    elif (algorithm == PCY):
        return pcy(datafile, minSupport, num_buckets, v=is_verbose)


def main():
    datafile, algorithm, minSupport, num_buckets, is_verbose, do_time = get_options()
    results = None

    if do_time:
        start = time.time()
        results = mine_data(algorithm, datafile, minSupport, num_buckets, is_verbose)
        print time.time() - start
    else:
        results = mine_data(algorithm, datafile, minSupport, num_buckets, is_verbose)

    print results
    return results

if __name__ == "__main__":
   main()