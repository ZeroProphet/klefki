import math


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


# from https://github.com/mikeivanov/paillier/blob/master/paillier/paillier.py

def invmod(a, p, maxiter=1000000):
    """The multiplicitive inverse of a in the integers modulo p:
         a * b == 1 mod p
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

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
