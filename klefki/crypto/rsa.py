"""
ref: https://www.wikiwand.com/zh-hans/%E8%BC%BE%E8%BD%89%E7%9B%B8%E9%99%A4%E6%B3%95
"""
from klefki.algorithms import extended_euclidean_algorithm
from klefki.numbers import lcm


__all__ = (
    "RSA",
    "mod_inverse",
)


def mod_inverse(a, m):
    """
    gcd = as + mt
    ab = 1 (mod m)
    a and m are relatively prime
    """
    g, s, t = extended_euclidean_algorithm(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return s % m


class RSA:
    """
    ref: https://www.wikiwand.com/en/RSA_(cryptosystem)
    You should always use encrypt and decrypt never use
    encrypt/decrypt with xxx-key without knowing what you are doing.
    """
    e = 65537

    def __init__(self, p, q):
        assert p > 0
        assert q > 0
        assert p != q
        self.n = p * q
        lambda_n = lcm((p - 1), (q - 1))
        assert lambda_n > self.e
        self.d = mod_inverse(self.e, lambda_n)

    @property
    def public_key(self):
        return self.n, self.e

    @property
    def private_key(self):
        return self.n, self.d

    def encrypt_with_pub_key(self, block: int):
        return pow(block, self.e, self.n)

    def decrypt_with_pub_key(self, block: int):
        return pow(block, self.e, self.n)

    def encrypt_with_private_key(self, block: int) -> int:
        return pow(block, self.d, self.n)

    def decrypt_with_private_key(self, block: int) -> int:
        return pow(block, self.d, self.n)

    encrypt_block = encrypt_with_pub_key
    decrypt_block = decrypt_with_private_key

    def encrypt_string(self, message: str) -> list:
        return [self.encrypt_with_pub_key(ord(x)) for x in message]

    def decrypt_string(self, encrypted: list):
        return ''.join([chr(self.decrypt_with_private_key(x)) for x in encrypted])
