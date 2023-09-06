from functools import reduce
from operator import add
from zkp_playground.algebra.utils import randfield


def additive_share(secret, F, n):
    shares = [randfield(F) for _ in range(n - 1)]
    shares += [(F(secret) - reduce(add, shares))]
    return shares


def additive_reconstruct(shares):
    return reduce(add, shares)
