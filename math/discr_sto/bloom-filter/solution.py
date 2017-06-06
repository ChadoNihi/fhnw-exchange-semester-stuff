class BloomFilter():
    def __init__(self, n_items_expected, p_err=0.01, print_stats = False):
        from math import log, ceil

        if p_err > 1 or p_err < 0:
            raise ValueError()

        if n_items_expected <= 0: n_items_expected = 1

        # formulas from https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions
        self.n_bits = ceil(  (n_items_expected * log(p_err)) / (log(2)**2)  )
        self.n_hashes = ceil(  -log(p_err) / log(2)  )

        self.bit_array = MyBitArray(n_bits)

        print('Bloom Filter of %d bits and %d hashes created\n(given %d expected items and P(false positive)=%.3f)'
                % (self.n_bits, self.n_hashes, n_items_expected, p_err))

    def insert(self, str):
        for i in self._get_indexes(str):
            self.bit_array.set_bit(i)

    def is_probably_exist(self, str):
        for i in self._get_indexes(str):
            if not self.bit_array.is_set(i): return False

        return True

    def _get_indexes(self, str):
        pass

    def _hash(self, val):
        pass

class MyBitArray():
    from math import ceil, floor

    def __init__(self, n_bits):
        self._byte_arr = bytearray(ceil(n_bits/8))

    def is_set(self, i):
        return (self._byte_arr[floor(i/8)] & (1<<idx)) != 0

    def set_bit(self, i):
        self._byte_arr[floor(i/8)] |= (1 << (i%8))

if __name__ == '__main__':
    in_fl_name = 'words.txt'

    # words = None
    with open(in_fl_name) as fl:
        words = fl.readlines()

    print(words)
