from itertools import islice, combinations
from collections import Counter, defaultdict

minSupport = 2681
minConfidence = 0.60


def get_n_baskets (file, n):
	array = []
	with open (file) as dataset:
		# return islice(dataset, n)
		for line in islice(dataset, n):
			array.append(line.rstrip('\n').split(' '))
	return array

def count_items (buckets) :
	c = Counter()

	for b in buckets:
		c.update(b)

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




baskets = get_n_baskets('dataset', 88000)
item_set = count_items(baskets)
del item_set['']
frequent = find_frequent_item_set(item_set, minSupport)
print frequent

doubles = list(combinations(frequent, 2))
tuple_count = count_items_tuples (doubles, baskets)
tuple_frequent = find_frequent_item_set(tuple_count, minSupport)
print tuple_frequent

triples = list(combinations(frequent, 3))
triple_count = count_items_triples (triples, baskets)
triple_frequent = find_frequent_item_set(triple_count, minSupport)
print triple_frequent
