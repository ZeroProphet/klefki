"""
ref: https://www.wikiwand.com/zh-hans/%E8%BC%BE%E8%BD%89%E7%9B%B8%E9%99%A4%E6%B3%95
"""
from klefki.const import SECP256K1_P, SECP256K1_N


def recursive_gcd(a, b):
    """
    辗转相除求a和b的最大公约数
    """
    assert a > b
    if b == 0:
        return a
    new_b = a % b
    new_a = b
    return recursive_gcd(new_a, new_b)


def iterative_gcd(a, b):
    assert a > b
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def iterative_extended_gcd(a, b):
    """
    a > b >=0
    gcd = as + bt
    return gcd, s, t
    ref: https://zhuanlan.zhihu.com/p/42707457
    ref: https://www.wikiwand.com/zh-hans/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95
    ref: https://codereview.stackexchange.com/questions/174336/rsa-algorithm-implementation-in-python-3
    """
    old_s, s = 1, 0
    old_t, t = 0, 1
    old_r, r = a, b
    if r == 0:
        return a, s, t
    else:
        while r != 0:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    """
    gcd = as + mt
    ab = 1 (mod m)
    a and m are relatively prime
    """
    g, s, t = iterative_extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return s % m


class RSA:
    """
    ref: https://www.wikiwand.com/zh-hans/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95
    """
    e = 65537

    def __init__(self, p, q):
        assert p > 0
        assert q > 0
        assert p != q
        self.n = p * q
        assert self.n > self.e
        self.r = (p - 1) * (q - 1)
        self.d = mod_inverse(self.e, self.r)

    @property
    def public_key(self):
        return self.n, self.e

    @property
    def private_key(self):
        return self.n, self.d

    def decrypt_block(self, block):
        return mod_inverse(block ** self.d, self.n)

    def encrypt_block(self, block):
        return mod_inverse(block ** self.e, self.n)

    def encrypt_string(self, message):
        return ''.join([chr(self.encrypt_block(int(x))) for x in message])

    def decrypt_string(self, encrypted):
        return ''.join([chr(self.decrypt_block(int(x))) for x in encrypted])


def test_rsa():
    rsa = RSA(SECP256K1_P, SECP256K1_N)
    string = "hello world"
    encrypted = rsa.encrypt_string(string)
    assert rsa.decrypt_string(encrypted) == string


assert recursive_gcd(1071, 462) == 21
assert iterative_gcd(1071, 462) == 21
assert iterative_gcd(3, 0) == 3
assert iterative_extended_gcd(1071, 462) == (21, -3, 7)
assert recursive_gcd(9, 6) == 3
assert iterative_gcd(9, 6) == 3
assert iterative_extended_gcd(9, 6) == (3, 1, -1)
assert iterative_extended_gcd(3, 0) == (3, 0, 1)
assert mod_inverse(5, 12) == 5
assert mod_inverse(23, 12) == 11
assert mod_inverse(23, 11) == 1

test_rsa()
