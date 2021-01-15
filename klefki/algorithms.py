from typing import Tuple, TypeVar, Iterable


__all__ = [
    'extended_euclidean_algorithm',
    'double_and_add_algorithm'
]

T = TypeVar('T')

def montgomery_multiplication(q):
    """
    Ref: https://hackmd.io/@zkteam/modular_multiplication
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
    pass


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
