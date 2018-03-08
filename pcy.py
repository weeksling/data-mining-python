from collections import Counter
from itertools import combinations, chain
from bitarray import bitarray

NUM_BUCKETS = 2000

def pcy(dataset, supportThreshold, num_buckets, v=False):
    global NUM_BUCKETS 
    NUM_BUCKETS = num_buckets
    
    frequent_items, hashvector, minSupport = find_frequent_items_and_hashvector(dataset, supportThreshold)
    
    if v:
        print "Frequent items length:", len(frequent_items)

    dataset.seek(0)
    candidate_doubles = get_candidate_doubles(frequent_items, hashvector, minSupport)
    frequent_doubles = find_frequent_doubles(dataset, candidate_doubles, supportThreshold)
    
    if v:
        print "Frequent double length:", len(frequent_doubles)

    dataset.seek(0)
    candidate_triples = get_candidate_triples(frequent_doubles)
    frequent_triples = find_frequent_triples(dataset, candidate_triples, supportThreshold)

    if v:
        print "Frequent triples length:", len(frequent_triples)

    all_frequent = frequent_items[:] + frequent_doubles[:] + frequent_triples[:]

    return all_frequent


def find_frequent_items_and_hashvector(dataset, supportThreshold):
    item_counts, num_buckets, hashmap = count_candidate_items_and_get_hashes(dataset)
    minSupport = num_buckets * supportThreshold

    hashvector = bitarray()
    for hash, count in hashmap.items():
        hashvector.append( count>minSupport )

    frequent_items = filter_frequent(item_counts, minSupport)
    return frequent_items, hashvector, minSupport



def count_candidate_items_and_get_hashes(dataset):
    counter = Counter()
    num_buckets = 0
    hash_counts = {}

    for line in dataset:
        num_buckets = num_buckets + 1
        items = parse_items(line)
        counter.update(items)
        
        #Hash and add to hashmap
        combos = list(combinations(items, 2))
        for combo in combos:
            hash = xor_hash(combo[0], combo[1], NUM_BUCKETS)
            if hash not in hash_counts:
                hash_counts[hash] = 1
            else:
                hash_counts[hash] += 1

    del counter['']
    return counter, num_buckets, hash_counts


def get_candidate_doubles(frequent_items, hashvector, minSupport):
    candidate_doubles = list(combinations(frequent_items, 2))

    for c in candidate_doubles:
        if hashvector[xor_hash(c[0], c[1], NUM_BUCKETS)] == '0':
            candidate_doubles.remove(c)

    return candidate_doubles


def find_frequent_doubles(dataset, candidate_doubles, supportThreshold):
    double_counts, num_buckets = count_candidate_doubles(dataset, candidate_doubles)
    minSupport = num_buckets * supportThreshold
    frequent_doubles = filter_frequent(double_counts, minSupport)
    return frequent_doubles


def count_candidate_doubles(dataset, candidates):
    d = {}
    num_buckets = 0

    for bucket in dataset:
        items = parse_items(bucket)
        num_buckets += 1
        for c in candidates:
            if c[0] in items and c[1] in items:
                if (c in d):
                    d[c] += 1
                else:
                    d[c] = 1
    return d, num_buckets

    
def get_candidate_triples(prev_frequent):
    flattened = list(set(chain.from_iterable(prev_frequent)))
    return list(combinations(flattened, 3))


def find_frequent_triples(dataset, candidate_triples, supportThreshold):
    triple_counts, num_buckets  = count_candidate_triples(dataset, candidate_triples)
    minSupport                  = num_buckets * supportThreshold
    frequent_triples            = filter_frequent(triple_counts, minSupport)
    return frequent_triples


def xor_hash (item1, item2, num_buckets):
    return (item1 ^ item2) % num_buckets


def count_candidate_triples(dataset, candidates):
    d = {}
    num_buckets = 0

    for bucket in dataset:
        items = parse_items(bucket)
        num_buckets += 1
        for c in candidates:
            if c[0] in items and c[1] in items and c[2] in items:
                if (c in d):
                    d[c] += 1
                else:
                    d[c] = 1
    return d, num_buckets


def parse_items(line):
    string_list = line.rstrip('\n').split(' ')
    cleaned_list = filter(None, string_list)
    return map(int, cleaned_list)


def filter_frequent(candidate_items, minSupport):
    for key, value in candidate_items.items():
        if (value < minSupport):
            del candidate_items[key]
    return candidate_items.keys()
