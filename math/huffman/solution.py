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

    pq = queue.PriorityQueue()

    for ch, cnt in counts.items():
        pq.put((cnt, ch))

    while pq.qsize() > 1:
        pass

def _huff_code_from_tree(node):
    # an explicit stack instead of recurssion to allow deeprer 'calls'
    recur_stack = [{
        'codes': {},
        'node': node
    }]
    virtual_params = None
    # logically do_while
    while True:
        # try-except is faster than `if` when the condition is rarely met: https://stackoverflow.com/a/2522013/4579279
        try:
            virtual_params = recur_stack.pop()
        except IndexError:
            break

    return virtual_params['codes']


if __name__ == '__main__':
    pass
