from typing import Tuple, TypeVar, Iterable
from zkp_playground.numbers import invmod
from functools import lru_cache


__all__ = [
    'extended_euclidean_algorithm',
    'double_and_add_algorithm'
]

T = TypeVar('T')


def bits(n: int) -> Iterable:
    """
    Generates the binary digits of n, starting
    from the least significant bit.
    bits(151) -> 1, 1, 1, 0, 1, 0, 0, 1
    """
    def _trans(n):
        while n:
            yield n & 1
            n >>= 1

    return _trans(n)


def bits_little_endian_from_bytes(s):
    return "".join([bin(ord(x))[2:].rjust(8, '0')[::-1] for x in s.decode()])


def bytes_from_bits_little_endian(s):
    return bytes([int(s[i:i+8][::-1], 2) for i in range(0, len(s), 8)])


def bytes_mul(a, b, s=32):
    t = [0] * 2 * s
    a = a.to_bytes(s, "big")[::-1]
    b = b.to_bytes(s, "big")[::-1]

    for i in range(0, s):
        C = 0
        for j in range(0, s):
            (C, S) = (t[i+j] + a[j] * b[i] + C).to_bytes(2, "big")
            t[i+j] = S
        t[i+s] = C
    return t[::-1]


@lru_cache(maxsize=None)
def montgomery_property(r, n):
    r_inv = invmod(r, n)
    return (r * r_inv - 1) // n


def mon_pro(a_, b_, r, n, n_):
    t = a_ * b_
    m = (t * n_) % r
    u_ = (t + m * n) // r
    if u_ >= n:
        return u_ - n
    else:
        return u_


def montgomery_mul(a, b, n):
    r = 2 ** (n.bit_length() + 1)
    n_ = montgomery_property(r, n)
    a_ = (a * r) % n
    b_ = (b * r) % n
    u_ = mon_pro(a_, b_, r, n, n_)
    return mon_pro(u_, 1, r, n, n_)


def CIOS(a, b, P, N=32):
    """
    # a[i], b[i], q[i] is the ith word of the numbers a,b,q
    # N is the number of machine words needed to store the modulus q
    Ref: https://hackmd.io/@zkteam/modular_multiplication
         https://www.microsoft.com/en-us/research/wp-content/uploads/1998/06/97Acar.pdf
    """

    a = a.to_bytes(N, "little")
    b = b.to_bytes(N, "little")
    q = P.to_bytes(N, "little")
    # R is set to the smallest power of two exceeding q that falls on a computer word boundary.
    # For example, if q is 381 bits then R=2^{6×64}=2^384 on a 64-bit architecture.
    # For zkp_playground, if q is 256 bits then R=2^{32x8}=2^256 on zkp_playground 8-bit(byte) implementation
    R = 2 ** (N*8)
    # D is the word size. For example, on a 64-bit architecture D is 2^64
    # For bytes, D is 2^8 = 256
    D = 2 ** 8
    # q'[0] is the lowest word of the number −q^{−1} mod R.
    #q_0 = list(int((-P**-1) % R).to_bytes(64, "little"))[0]
    FieldR = type("Field", (FiniteField, ), dict(P=R))
    q_0 = ((-(~FieldR(F.P))).value).to_bytes(N, "little")[0]
    # t is a temporary array of size N+2
    t = [0] * (N + 2)

    for i in range(0, N):
        # cal multi
        C = 0
        for j in range(0, N):
            (C, t[j]) = (t[j] + a[j] * b[i] + C).to_bytes(2, "big")
        (t[N+1], t[N]) = (t[N] + C).to_bytes(2, "big")

        # cal mod
        C = 0
        m = (t[0] * q_0) % D
        (C, _) = (t[0] + m * q[0]).to_bytes(2, "big")
        for j in range(1, N):
            (C, t[j-1]) = (t[j] + m * q[j] + C).to_bytes(2, "big")
        (C, t[N-1]) = (t[N] + C).to_bytes(2, "big")
        t[N] = t[N+1] + C
    return int.from_bytes(t, "little")


def complex_truediv_algorithm(x: complex, y: complex, f: T) -> T:
    a = f(x.real)
    b = f(x.imag)
    c = f(y.real)
    d = f(y.imag)

    return f(complex(
        (a*c + b*d) / (c**2 + d**2),
        (b*c - a*d) / (c**2 + d**2)
    ))


def extended_euclidean_algorithm(a: int, b: int, one=1, zero=0) -> Tuple[int, int, int]:
    '''
    Returns a three-tuple (gcd, x, y) such that
    a * x + b * y == gcd, where gcd.

    This function implements the extended Euclidean
    algotithm and runs in O(log b) in the worst case
    '''
    s, t, r = zero, one, b
    old_s, old_t, old_r = one, zero, a

    while r != zero:
        quoient = old_r // r
        old_r, r = r, old_r - quoient * r
        old_s, s = s, old_s - quoient * s
        old_t, t = t, old_t - quoient * t
    return old_r, old_s, old_t


def double_and_add_algorithm(times: int, x: T, init: T) -> T:
    """
    Returns the result of n * x, computed using
    the double and add algorithm.
    """

    result = init
    addend = x

    for bit in bits(times):
        if bit == 1:
            result = addend + result
        addend = addend + addend

    return result


def fast_pow(times: int, x: T, init: T) -> T:
    result = init
    addend = x

    for bit in bits(times):
        if bit == 1:
            result = addend * result
        addend = addend * addend
    return result


def newton_iterator_sqrt(x: T):
    if (x.value == 0):
        return x
    last = x.__class__(0)
    res = x.__class__(1)
    while res != last:
        last = res
        res = (res + x / res) / x.__class__(2)
    return res


def lagrange_polynomial(xs, ys, field=int):
    k = len(xs)

    def l(j): return lambda x: reduce(
        mul, [(x-xs[m])/(xs[j]-xs[m]) for m in range(0, k) if m != j])

    return lambda x: field(reduce(add, [ys[j] * l(j)(x) for j in range(0, k)]))
