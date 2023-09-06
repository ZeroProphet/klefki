import math
from functools import reduce
from operator import mul

# https://crypto.stackexchange.com/questions/29591/lcm-versus-phi-in-rsa


def rsa_lambda(p, q):
    return lcm(p-1, q-1)


def rsa_phi(p, q):
    return (p-1) * (q-1)


def fn_lambda(n):
    '''
    Carmichael Function
    A number n is said to be a Carmichael number if
    it satisfies the following modular arithmetic condition:
    power(b, n-1) MOD n = 1,
    for all b ranging from 1 to n such that b and
    n are relatively prime, i.e, gcd(b, n) = 1
    '''
    coprimes = [x for x in range(1, n) if math.gcd(x, n) == 1]
    k = 1
    while not all(pow(x, k, n) == 1 for x in coprimes):
        k += 1
    return k


def fn_phi(n):
    '''
    Eulers Totient Function
    https://stackoverflow.com/questions/18114138/computing-eulers-totient-function
    '''
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount


carmichael = fn_lambda
totient = fn_phi


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def length(n, base=10):
    return math.floor(math.log(n, base)) + 1


def Blength(n, base=2):
    return math.floor(math.log(n, base)) + 1


def Dlength(n, base=10):
    return math.floor(math.log(n, base)) + 1


def power(base, exp):
    """ Fast power calculation using repeated squaring """
    if exp < 0:
        return 1 / power(base, -exp)
    ans = 1
    while exp:
        if exp & 1:
            ans *= base
        exp >>= 1
        base *= base
    return ans


def invmod(a, p):
    from zkp_playground.types.algebra.meta import field
    f = field(p)
    return (~f(a)).value


def modpow(base, exponent, modulus):
    """Modular exponent:
         c = b ^ e mod m
       Returns c.
       (http://www.programmish.com/?p=34)"""
    result = 1
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def modular_sqrt(a, p):
    """
    ref: https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
    Find a quadratic residue (mod p) of 'a'. p
    must be an odd prime.
    Solve the congruence of the form:
    x^2 = a (mod p)
    And returns x. Note that p - x is also a root.
    0 is returned is no square root exists for
    these a and p.
    The Tonelli-Shanks algorithm is used (except
    for some simple cases in which the solution
    is known from an identity). This algorithm
    runs in polynomial time (unless the
    generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
    Euler's criterion. p is a prime, a is
    relatively prime to p (if p divides
    a, then a|p = 0)
    Returns 1 if a has a square root modulo
    p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def crt(a_list, n_list) -> int:
    """Applies the Chinese Remainder Theorem to find the unique x such that x = a_i (mod n_i) for all i.
    :param a_list: A list of integers a_i in the above equation.
    :param n_list: A list of integers b_i in the above equation.
    :return: The unique integer x such that x = a_i (mod n_i) for all i.
    copy from::
    https://github.com/cryptovoting/damgard-jurik/blob/master/damgard_jurik/utils.py#L100
    """
    a_list = [a_i for a_i in a_list]
    n_list = [n_i for n_i in n_list]

    N = reduce(mul, n_list)
    y_list = [N // n_i for n_i in n_list]
    z_list = [invmod(y_i, n_i) for y_i, n_i in zip(y_list, n_list)]
    x = sum(a_i * y_i * z_i for a_i, y_i, z_i in zip(a_list, y_list, z_list))

    return x
