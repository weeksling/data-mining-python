from itertools import islice, combinations, chain
from collections import Counter, defaultdict
import time

minSupport = 2644.86 #2681
minConfidence = 0.60


def get_n_baskets (dataset, n):
	array = []
	# return islice(dataset, n)
	for line in islice(dataset, n):
		array.append(line.rstrip('\n').split(' '))
	return array

def get_item_counts (buckets) :
	c = Counter()

	for b in buckets:
		c.update(b)

	del c['']
	return c

def count_items_tuples (tuples, baskets):
	d = {}

	for b in baskets:
		for t in tuples:
			if t[0] in b and t[1] in b:
				if (t in d):
					d[t] += 1
				else:
					d[t] = 1
	return d

def count_items_triples (tuples, baskets):
	d = {}

	for b in baskets:
		for t in tuples:
			if t[0] in b and t[1] in b and t[2] in b:
				if (t in d):
					d[t] += 1
				else:
					d[t] = 1
	return d

def find_frequent_item_set (candidate_item_set, min_threshold):
	for key, value in candidate_item_set.items():
		if (value < min_threshold):
			del candidate_item_set[key]

	return candidate_item_set.keys()

def apriori_no_flattening (baskets):
	item_set = get_item_counts(baskets)
	frequent = find_frequent_item_set(item_set, minSupport)
	print "items length:", len(frequent)

	doubles = list(combinations(frequent, 2))
	tuple_count = count_items_tuples (doubles, baskets)
	tuple_frequent = find_frequent_item_set(tuple_count, minSupport)
	print "tuple length:", len(tuple_frequent)

	triples = list(combinations(frequent, 3))

	triple_count = count_items_triples (triples, baskets)
	triple_frequent = find_frequent_item_set(triple_count, minSupport)
	print triple_frequent
	print "triple length:", len(triple_frequent)

def apriori_with_flattening (baskets):
	item_set = get_item_counts(baskets)
	frequent = find_frequent_item_set(item_set, minSupport)
	
	print "items length:", len(frequent)

	doubles = list(combinations(frequent, 2))
	tuple_count = count_items_tuples (doubles, baskets)
	tuple_frequent = find_frequent_item_set(tuple_count, minSupport)
	
	print "tuple length:", len(tuple_frequent)


	flattened = list(set(chain.from_iterable(tuple_frequent)))
	triples = list(combinations(flattened, 3))
	triple_count = count_items_triples (triples, baskets)
	triple_frequent = find_frequent_item_set(triple_count, minSupport)

	print "triple length:", len(triple_frequent)


def apriori (dataset, minSupport):
	baskets = get_n_baskets(dataset, None)

	# start = time.time()
	# apriori_no_flattening(baskets)
	# print 'elapsed', time.time() - start

	apriori_with_flattening(baskets)


