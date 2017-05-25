def count_chars(str):
    chars = list(str)
    counts = dict()
    for ch in chars:
        counts[ch] = (1 if ch not in counts else counts[ch]+1)

    return counts

def get_chars_freq(str):
    counts = count_chars(str)
    total = len(str)
    return {ch: cnt / total for (ch, cnt) in counts}

def huff_code_from_freq(freq):
    pass

if __name__ == '__main__':
    pass
