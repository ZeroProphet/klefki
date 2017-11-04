from typing import Tuple, TypeVar, Iterable


__all__ = [
    'extended_euclidean_algorithm',
    'double_and_add_algorithm'
]

T = TypeVar('T')


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
