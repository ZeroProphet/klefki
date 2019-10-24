import math


def carmichael(n):
    '''
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



def lcm(a, b):
    return abs(a*b) // gcd(a, b)


def len(n, base=10):
    return math.floor(math.log(n, base)) + 1


def Blen(n, base=2):
    return math.floor(math.log(n, base)) + 1


def Dlen(n, base=10):
    return math.floor(math.log(n, base)) + 1
