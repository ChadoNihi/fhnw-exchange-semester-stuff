from math import ceil, floor, log
try:
    import mmh3
except ImportError:
    raise ImportError("Cannot import module 'mmh3'. Try to install it with 'pip install mmh3'")

class BloomFilter():
    def __init__(self, n_items_expected, p_err=0.01, print_stats = False):
        if p_err > 1 or p_err < 0:
            raise ValueError()

        if n_items_expected <= 0: n_items_expected = 1

        # formulas from https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions
        self.n_bits = ceil(  -(n_items_expected * log(p_err)) / (log(2)**2)  )
        self.n_hashes = ceil(  -log(p_err) / log(2)  )

        self.bit_array = MyBitArray(self.n_bits)

        if print_stats: print('Bloom Filter of %d bits and %d hashes created\n(given %d expected items and P(false positive)=%.3f)'
                % (self.n_bits, self.n_hashes, n_items_expected, p_err))

    def insert(self, s):
        for i in self._get_indexes(s):
            self.bit_array.set_bit(i)

    def is_probably_exist(self, s):
        for i in self._get_indexes(s):
            if not self.bit_array.is_set(i): return False

        return True

    def _get_indexes(self, s):
        return [self._hash(s, seed) % self.n_bits for seed in range(self.n_hashes)]

    def _hash(self, val, seed=None):
        return mmh3.hash(val, seed) if seed else mmh3.hash(val)

class MyBitArray():
    def __init__(self, n_bits):
        self._byte_arr = bytearray(ceil(n_bits/8))

    def is_set(self, i):
        return (self._byte_arr[floor(i/8)] & (1<<(i%8))) != 0

    def set_bit(self, i):
        self._byte_arr[floor(i/8)] |= (1 << (i%8))

    def __str__(self):
        return str(self._byte_arr)

if __name__ == '__main__':
    import random as rand
    words_fl_name = 'words.txt'

    with open(words_fl_name) as fl:
        contents = fl.readlines()
        words = [line.rstrip('\n') for line in contents]

    n_words = len(words)
    fp_prob = 0.01
    bloom_filter = BloomFilter(n_words, p_err=fp_prob, print_stats = True)

    for w in words:
        bloom_filter.insert(w)
        if not bloom_filter.is_probably_exist(w):
            raise ValueError(w)

    # testing actual error ratio
    n_false_positives = 0
    n_rand_strs = n_words
    rand_ints = rand.sample(range(100, 99999999), n_rand_strs)
    for rand_str in (str(rand_int) for rand_int in rand_ints):
        # checking a random int string, which is not in the filter
        if bloom_filter.is_probably_exist(rand_str):
            n_false_positives += 1

    print('\nRequested probability of a false positive: %.4f\nActual error after testing on %d random strings: %.4f'
            % (fp_prob, n_rand_strs, n_false_positives/n_rand_strs))
