from functools import lru_cache
from klefki.numbers import invmod
from math import factorial

def damgard_jurik_reduce(a: int, s: int, n: int) -> int:
    """Computes i given a = (1 + n)^i (mod n^(s+1)).
    :param a: The integer a in the above equation.
    :param s: The integer s in the above equation.
    :param n: The integer n in the above equation.
    :return: The integer i in the above equation.
    """
    def L(b: int) -> int:
        assert (b - 1) % n == 0
        return (b - 1) // n

    @lru_cache(int(s))
    def n_pow(p: int) -> int:
        return n ** p

    @lru_cache(int(s))
    def fact(k: int) -> int:
        return factorial(k)

    i = 0
    for j in range(1, s + 1):

        t_1 = L(a % n_pow(j + 1))
        t_2 = i

        for k in range(2, j + 1):
            k = k

            i = i - 1
            t_2 = t_2 * i % n_pow(j)
            t_1 = t_1 - (t_2 * n_pow(k - 1) * invmod(fact(k), n_pow(j))) % n_pow(j)

        i = t_1
    return i
