from itertools import islice, combinations, chain
from collections import Counter, defaultdict
from bitarray import bitarray


minSupport = 2681
minConfidence = 0.60
NUM_BUCKETS = 50


def xor_hash (item1, item2, num_buckets):
    return (item1 ^ umber(item2)) % num_buckets

def get_n_baskets (file, n):
	array = []
	with open (file) as dataset:
		# return islice(dataset, n)
		for line in islice(dataset, n):
			array.append(line.rstrip('\n').split(' '))
	return array

def count_items_and_hashes (buckets):
	item_count = Counter()
	hash_counts = {}


	for b in buckets:
		#Hash and add to hashmap
		combos = list(combinations(b, 2))
		for combo in combos:
			hash = xor_hash(combo[0], combo[1], NUM_BUCKETS)
			if (hash_counts[hash]!=None):
				hash_counts[hash] = 1
			else:
				hash_counts[hash] += 1
		
		#Count each item in basket
		item_count.update(b)

	#remove unnecessary 
	del item_counts['']
	return item_counts, hash_counts
		

def find_frequent_item_set (candidate_item_set, min_threshold):
	for key, value in candidate_item_set.items():
		if (value < min_threshold):
			del candidate_item_set[key]

	return candidate_item_set.keys()

def pcy (dataset, minSupport):
	print 'pcy not implemented yet'
	pass

# baskets = get_n_baskets('dataset', 88000)
# item_counts, hash_counts = count_items_and_hashes(baskets)
# frequent_items = find_frequent_item_set(item_counts, minSupport)

# doubles = list(combinations(frequent_items, 2))

# candidate_vector = get_candidate_bit_vector(doubles, baskets)

