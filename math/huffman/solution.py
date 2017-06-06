class HuffmanNode():
    def __init__(self, l=None, r=None, val=None):
        self.l = l
        self.r = r
        self.val = val

    # for compatibility w/ ordering within PriorityQueue
    def __lt__(self, other):
        return 0

def count_chars(s):
    chars = list(s)
    counts = dict()
    for ch in chars:
        counts[ch] = (1 if ch not in counts else counts[ch]+1)

    counts['total_count'] = len(s)

    return counts

def encode_str(s, codes = None):
    if not codes: codes = huff_code_from_counts(count_chars(s))

    return ''.join(''.join(str(c) for c in codes[ch]) for ch in s)

def extend_bin_code(s):
    return s + '1' + '0'*((len(s)+1) % 8)

# def get_chars_freq(s):
#     counts = count_chars(s)
#     total = len(s)
#     return {ch: cnt / total for (ch, cnt) in counts}

def huff_code_from_counts(counts):
    import queue

    pq = queue.PriorityQueue()

    for ch, cnt in counts.items():
        if ch == 'total_count': continue
        pq.put((cnt, HuffmanNode(val = ch)))

    while pq.qsize() > 1:
        l_freq_node_pair, r_freq_node_pair = pq.get(), pq.get()

        pq.put(
            (
                l_freq_node_pair[0] + r_freq_node_pair[0],
                HuffmanNode(l_freq_node_pair, r_freq_node_pair)
            )
        )

    return _huff_code_from_tree(pq.get())

def store_codes_in_file(codes, fl_name = 'dec_tab.txt'):
    with open(fl_name, 'w') as out_fl:
        out_list = []
        sorted_kv = sorted(codes.items())
        for ch, code in sorted_kv:
            out_list.append(str(ord(ch)) + ':' + ''.join(str(c) for c in code))

        out_fl.write('-'.join(out_list))

def write_bytearray(byteseq, out_fl_name='output.dat'):
    with open(out_fl_name, 'wb') as out_fl:
        out_fl.write(byteseq)

def _huff_code_from_tree(node):
    # an explicit stack instead of recurssion to allow deeprer 'calls'
    recur_stack = [{
        'prefix': [],
        'node': node
    }]
    virt_params = None
    codes = {}
    # logically do_while
    while True:
        # try-except is faster than `if` when the condition is rarely met: https://stackoverflow.com/a/2522013/4579279
        try:
            virt_params = recur_stack.pop()
        except IndexError:
            break

        l = virt_params['node'][1].l
        if not l[1].val:
            virt_params['prefix'].append(0)
            recur_stack.append({
                'prefix': virt_params['prefix'],
                'node': l
            })
        else:
            codes[l[1].val] = virt_params['prefix'] + [0]

        r = virt_params['node'][1].r
        if not r[1].val:
            virt_params['prefix'].append(1)
            recur_stack.append({
                'prefix': virt_params['prefix'],
                'node': r
            })
        else:
            codes[r[1].val] = virt_params['prefix'] + [1]

    return codes

if __name__ == '__main__':
    infile_name = 'input.txt'

    infile_obj = open(infile_name)
    in_str = infile_obj.read()

    counts = count_chars(in_str)

    infile_obj.close()

    print('Input string:\n', in_str, '\n')
    print('Char frequencies:\n', counts, '\n')

    codes = huff_code_from_counts(counts)
    print('Codes:\n', codes, '\n')

    store_codes_in_file(codes)

    extended_encoded_input_str = extend_bin_code(encode_str(in_str, codes))
    print('(Extended) encoded input string:\n', extended_encoded_input_str, '\n')

    write_bytearray(bytearray(extended_encoded_input_str, encoding='ascii'))

    # print(open('output.dat', 'rb').read().decode('utf-8'))
