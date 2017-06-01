# class HuffmanNode():
#     def __init__(self, l=None, r=None):
#         self.l = l
#         self.r = r
#
#     # for compatibility w/ ordering within PriorityQueue
#     def __lt__(self, other):
#         return 0

def count_chars(str):
    chars = list(str)
    counts = dict()
    for ch in chars:
        counts[ch] = (1 if ch not in counts else counts[ch]+1)

    counts['total_count'] = len(str)

    return counts

# def get_chars_freq(str):
#     counts = count_chars(str)
#     total = len(str)
#     return {ch: cnt / total for (ch, cnt) in counts}

def huff_code_from_counts(counts):
    import queue
    queue.PriorityQueue._old_put = queue.PriorityQueue._put
    queue.PriorityQueue._put = _put
    pq = queue.PriorityQueue()

    for ch, cnt in counts.items():
        pq.put((cnt, ch))

    while pq.qsize() > 1:
        l_freq_node_pair, r_freq_node_pair = pq.get(), pq.get()

        pq.put(
            (
                l_freq_node_pair[0] + r_freq_node_pair[0],
                {'l': l_freq_node_pair, 'r': r_freq_node_pair}
            )
        )

    return _huff_code_from_tree(pg.get())

def _huff_code_from_tree(node):
    # an explicit stack instead of recurssion to allow deeprer 'calls'
    recur_stack = [{
        'codes': {},
        'prefix': [],
        'node': node
    }]
    virtual_params = None
    # logically do_while
    while True:
        # try-except is faster than `if` when the condition is rarely met: https://stackoverflow.com/a/2522013/4579279
        try:
            virt_params = recur_stack.pop()
        except IndexError:
            break

        l, r = virt_params['node'][1]['l'], virt_params['node'][1]['r']

        if isinstance(l[1], dict):
            recur_stack.push({
                'codes': virt_params['codes'],
                'prefix': virt_params['prefix'].append(0),
                'node': l
            })
        else:
            virt_params['codes'][l[1]] = virt_params['prefix'].append(0)

        if isinstance(r[1], dict):
            recur_stack.push({
                'codes': virt_params['codes'],
                'prefix': virt_params['prefix'].append(1),
                'node': r
            })
        else:
            virt_params['codes'][r[1]] = virt_params['prefix'].append(1)

    return virtual_params['codes']

def _put(self, pair):
    self._old_put(pair)


if __name__ == '__main__':
    infile_name = 'input.txt'

    infile_obj = open(infile_name)

    counts = count_chars(infile_obj.read())

    infile_obj.close()

    print(counts)
    print()

    codes = huff_code_from_counts(counts)
    print(codes)
