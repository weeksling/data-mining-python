from collections import Counter
from itertools import combinations, chain

def pcy(dataset, supportThreshold):
    frequent_items = find_frequent_items(dataset, supportThreshold)
    
    print "Frequent items length:", len(frequent_items)

    dataset.seek(0)
    candidate_doubles = get_candidate_doubles(frequent_items)
    frequent_doubles = find_frequent_doubles(dataset, candidate_doubles, supportThreshold)
    
    print "Frequent double length:", len(frequent_doubles)

    dataset.seek(0)
    candidate_triples = get_candidate_triples(frequent_doubles)
    frequent_triples = find_frequent_triples(dataset, candidate_triples, supportThreshold)

    print frequent_triples
    print "Frequent triples length:", len(frequent_triples)

    all_frequent = []
    all_frequent.append(frequent_items[:])
    all_frequent.append(frequent_doubles[:])
    all_frequent.append(frequent_triples[:])
    return all_frequent


def find_frequent_items(dataset, supportThreshold):
    item_counts, num_buckets = count_candidate_items(dataset)
    minSupport = num_buckets * supportThreshold
    frequent_items = filter_frequent(item_counts, minSupport)
    return frequent_items


def find_frequent_doubles(dataset, candidate_doubles, supportThreshold):
    double_counts, num_buckets = count_candidate_doubles(dataset, candidate_doubles)
    minSupport = num_buckets * supportThreshold
    frequent_doubles = filter_frequent(double_counts, minSupport)
    return frequent_doubles


def find_frequent_triples(dataset, candidate_triples, supportThreshold):
    triple_counts, num_buckets  = count_candidate_triples(dataset, candidate_triples)
    minSupport                  = num_buckets * supportThreshold
    frequent_triples            = filter_frequent(triple_counts, minSupport)
    return frequent_triples


def count_candidate_items(dataset):
    counter = Counter()
    num_buckets = 0

    for line in dataset:
        num_buckets = num_buckets + 1
        items = parse_items(line)
        counter.update(items)

    del counter['']
    return counter, num_buckets


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


def get_candidate_doubles(frequent_items):
    return list(combinations(frequent_items, 2))


def get_candidate_triples(prev_frequent):
    flattened = list(set(chain.from_iterable(prev_frequent)))
    return list(combinations(flattened, 3))


def filter_frequent(candidate_items, minSupport):
    for key, value in candidate_items.items():
        if (value < minSupport):
            del candidate_items[key]
    return candidate_items.keys()
