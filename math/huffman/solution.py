

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


if __name__ == '__main__':
    pass
