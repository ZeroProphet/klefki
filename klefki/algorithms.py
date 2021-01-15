from typing import Tuple, TypeVar, Iterable
from ctypes import c_uint64 as uint64
from math import log2

__all__ = [
    'extended_euclidean_algorithm',
    'double_and_add_algorithm'
]

T = TypeVar('T')

def CIOS(a, b, P):
    """
    Ref: https://hackmd.io/@zkteam/modular_multiplication
         https://www.microsoft.com/en-us/research/wp-content/uploads/1998/06/97Acar.pdf
    The Montgomery multiplication algorithm does not directly compute abmodq.
    Instead it computes abR^{−1} mod q for some carefully chosen number R called the Montgomery radix.
    Typically, R is set to the smallest power of two exceeding q that falls on a computer word boundary.
    For example, if q is 381 bits then R=26×64=2384 on a 64-bit architecture.

    In order to make use of Montgomery multiplication the numbers a,b must be encoded into Montgomery form:
    instead of storing a,b, we store the numbers ~a,~b given by

    ~a=aR mod q
    ~b=bR mod q

    A simple calculation shows that Montgomery multiplication produces the product abmodq,
    also encoded in Montgomery form:
    (aR)(bR)R^{−1}=abR mod q
    The idea is that numbers are always stored in Montgomery form so as to
    avoid costly conversions to and from Montgomery form.
    """

    from klefki.types.algebra.fields import FiniteField

    def split(x, words=4):
        bt = x.to_bytes(words * 8, "big")
        for i in range(0, int(len(bt) / 8)):
            yield uint64(int.from_bytes(bt[0 + i * 8: 8 + i* 8], "big"))

    a = list(split(a))
    b = list(split(b))
    q = list(split(P))
    N = len(q)
    R = 2 ** (N * 64)
    D = 2 ** 64
    Field = type("Field", (FiniteField, ), dict(P=R))
    q_0 = list(split((-(FJ(F.P) ** (-1))).value))[0]
    t = (uint64 * (N + 2))()

    for i in range(0, N):
        C = uint64(0)
        for j in range(0, N):
            (C, t[j]) = split(t[j] + a[j].value * b[i].value + C.value, 2)

        (t[N + 1], t[N]) = split(t[N] + C.value, 2)

        C = uint64(0)
        m = (t[0] * q_0.value) % D
        (C, _) = split(t[0] + m * q_0.value, 2)

        for j in range(1, N):
            (C, t[j-1]) = split(t[j] + m * q[j].value + C.value, 2)

        (C, t[N-1]) = split(t[N] + C.value, 2)
        t[N] = t[N+1] + C.value

    return t


def complex_truediv_algorithm(x: complex, y: complex, f: T) -> T:
    a = f(x.real)
    b = f(x.imag)
    c = f(y.real)
    d = f(y.imag)

    return f(complex(
        (a*c + b*d) / (c**2 + d**2),
        (b*c - a*d) / (c**2 + d**2)
    ))


def extended_euclidean_algorithm(a: int, b: int) -> Tuple[int, int, int]:
    '''
    Returns a three-tuple (gcd, x, y) such that
    a * x + b * y == gcd, where gcd.

    This function implements the extended Euclidean
    algotithm and runs in O(log b) in the worst case
    '''
    s, t, r = 0, 1, b
    old_s, old_t, old_r = 1, 0, a

    while r != 0:
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
    def bits(n: int) -> Iterable:
        """
        Generates the binary digits of n, starting
        from the least significant bit.
        bits(151) -> 1, 1, 1, 0, 1, 0, 0, 1
        """
        while n:
            yield n & 1
            n >>= 1

    result = init
    addend = x

    for bit in bits(times):
        if bit == 1:
            result = addend + result
        addend = addend + addend

    return result


def newton_iterator_sqrt(x: T):
    if (x.value == 0): return x
    last = x.__class__(0)
    res = x.__class__(1)
    while res != last:
        last = res
        res = (res + x / res) / x.__class__(2)
    return res
