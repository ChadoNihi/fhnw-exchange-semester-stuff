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

def _huff_code_from_tree(node):
    # an explicit stack instead of recurssion to allow deeprer 'calls'
    recur_stack = [{
        'codes': {},
        'node': node
    }]
    # logically do_while
    while True:
        try:
            virtual_params = recur_stack.pop()
        except IndexError:
            break

    return codes


if __name__ == '__main__':
    pass
