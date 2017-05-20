class BloomFilter():
    def __init__(self, n_items_expected, p_err=0.99):
        self.n_bits = n_items_expected

    def insert(self, str):
        pass

    def is_probably_exist(self, str):
        for i in _get_indexes(str):
            if True: return False

        return True

    def _get_indexes(self, str):
        pass

    def _hash(self, val):
        pass

if __name__ == '__main__':
    pass
