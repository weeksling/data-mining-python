# Data Mining Python library

This library implements basic data mining for disk-bound data. 
Featuring two algorithms: A-Priori, and Park-Chen-Yu (PCY).

## Requirements
Python 2.7

## Usage
```
usage: datamining.py [-h] [-a {APRIORI,PCY}] [-s SUPPORT] datafile

positional arguments:
  datafile              The name of the file to be mined for data

optional arguments:
  -h, --help            show this help message and exit
  -a {APRIORI,PCY}, --alg {APRIORI,PCY}
                        Name of algorithm to be used. Options: 'PCY' or
                        'APRIORI'. Default: 'APRIORI'
  -s SUPPORT, --support SUPPORT
                        The minimum % of buckets a candidate must be in to be
                        accepted (ex: 0.03)

python datamine.py --support=[% of buckets] --alg=[PCY | APRIORI, default=APRIORI] datafile
```
