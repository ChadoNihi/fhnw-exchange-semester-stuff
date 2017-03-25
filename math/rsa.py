from math import gcd
from random import getrandbits, randint # getrandbits returns an int with k random bits

def rsa_gen_e_d_n(approx_key_bit_len = 16):
    if approx_key_bit_len < 16:
        print('Warning: key bit length is too small (%d), setting it to 16.' % approx_key_bit_len)
        approx_key_bit_len = 16

    p = next_prime(int("1" + bin(getrandbits( (approx_key_bit_len // 2)-3 ))[2:], 2)) # next prime of a random (approx_key_bit_len-2)-bit int. [2:] is for dropping '0b' of bin() result (e.g. 'ob10011' -> '10011')
    q = next_prime(int("1" + bin(getrandbits( (approx_key_bit_len // 2)+2 ))[2:], 2))
    print('p: %d, q: %d' % (p,q))
    n = p*q
    lambda_n = lcm(p-1, q-1) # lambda_n is an alternative to phi_n

    e = 13
    while gcd(e, lambda_n) != 1:
        e += 2

    if e >= lambda_n:
        raise RuntimeError("e must be < lambda_n: e == %f, lambda_n == %f" % (e, lambda_n))

    d = get_d(e, n)

    with open('pk.txt', 'w') as fl:
        fl.write('(%d, %d)' % (n, e))
        print('Public key (n: %d, e: %d) is stored in pk.txt' % (n, e))

    with open('sk.txt', 'w') as fl:
        fl.write('(%d, %d)' % (n, d))
        print('Private key (n: %d, d: %d) is stored in sk.txt' % (n, d))

    return {"e": e, "d": d, "n": n}

def encrypt_text(text, e, n, cipher_flname = 'cipher.txt'):
    with open(cipher_flname, 'a') as fl:
        for ch in text:
            fl.write( encrypt(ord(ch), e, n) )

def decrypt_text(cipher, d, n, decrypted_text_flname = 'text-d.txt'):
    cipher_codes = map(int, cipher.split(','))
    with open(decrypted_text_flname, 'a') as fl:
        for c in cipher_codes:
            fl.write( chr(decrypt(c, d, n)) )

# HELPER FUNCTIONS:

def encrypt(m, e, n):
    return mod_pow(m, e, n)

def decrypt(c, d, n):
    return mod_pow(c, d, n)

def get_d(e, n):
    # Extended Euclidean algorithm
    a, b = ((e, n) if e > n else (n, e))
    x0, y0, x1, y1 = 1, 0, 0, 1

    while b > 0:
        r = a % b
        q = a // b
        a = b
        b = r
        prev_x0, prev_y0 = x0, y0
        x0, y0 = x1, y1
        x1 = prev_x0 - q*x1
        y1 = prev_y0 - q*y1

    # d must not be negative.
    # (n+y0) % n == y0 % n, for y0 < 0
    return n+y0 if y0 < 0 else y0

def lcm(a, b):
    # lcm(0,0) is a special case
    return 0 if a==0 and b==0 else abs(a*b) // gcd(a,b)

def mod_pow(base, exp, mod):
    if mod == 1: return 0

    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result*base) % mod
        base = (base*base) % mod
        exp >>= 1 # exp = right bit shift old exp

    return result

def next_prime(x):
    # adopted from http://stackoverflow.com/a/30778549/4579279
    if x < 2: return 2
    if x < 3: return 3
    if x < 5: return 5

    x += (1 if x % 2 == 0 else 2)
    while not is_probably_prime(x):
        # all prime numbers > 5 are of the form 30k + i for i = 1, 7, 11, 13, 17, 19, 23, 29 (https://en.wikipedia.org/wiki/Primality_test#Simple_methods)
        x += [1,6,5,4,3,2,1,4,3,2,1,2,1,4,3,2,1, \
              2,1,4,3,2,1,6,5,4,3,2,1,2][x % 30]
    return x

def is_probably_prime(cand, k = 7): # Miller–Rabin primality test. Adapted from http://stackoverflow.com/a/30778549/4579279
    if cand < 2: return False

    # try fast screening
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if cand % p == 0: return cand == p

    # the algorithm
    s, d = 0, cand-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(randint(2, cand-1), d, cand)
        if x == 1 or x == cand-1: continue
        for r in range(1, s):
            x = (x * x) % cand
            if x == 1: return False
            if x == cand-1: break
        else: return False
    return True

def read_key(flname):
    with open(flname, 'r') as fl:
        import re
        num_re = re.compile('\d+')

        return list(map(int, re.findall(num_re, fl.read())[:2]))

# executes when the file is run as a script (as opposed being imported as a module)
if __name__ == "__main__":
    from sys import argv

    num_argv = len(argv)
    usage_msg = """Program usage:
    - To generate RSA key pair (default is 1024): <script_name>.py gen [key_bit_length]
    - To encrypt a file (default is text.txt into cipher.txt): <script_name>.py enc [text.txt cipher.txt]
    - To decrypt a file (default is cipher.txt to text-d.txt): <script_name>.py dec [cipher.txt text-d.txt]\n"""

    if num_argv <= 1 or argv[1] == '-h' or argv[1] == '--help' or argv[1] == 'help':
        print(usage_msg)

    elif argv[1].startswith('gen'):
        if num_argv >= 3:
            rsa_gen_e_d_n(int(argv[2]))
        else:
            rsa_gen_e_d_n()

    elif argv[1].startswith('enc'):
        n_e = read_key('pk.txt')
        with open(('text.txt' if num_argv < 3 else argv[2]), 'r') as fl:
            if num_argv >= 4:
                encrypt_text(fl.read(), n_e[1], n_e[0], argv[3])
            else:
                encrypt_text(fl.read(), n_e[1], n_e[0])

    elif argv[1].startswith('dec'):
        n_d = read_key('sk.txt')
        with open(('cipher.txt' if num_argv < 3 else argv[2]), 'r') as fl:
            if num_argv >= 4:
                decrypt_text(fl.read(), n_d[1], n_d[0], argv[3])
            else:
                decrypt_text(fl.read(), n_d[1], n_d[0])

    else:
        print(usage_msg)
