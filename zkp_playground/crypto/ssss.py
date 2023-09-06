'''
* ref https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
The essential idea of Adi Shamir's threshold scheme is that 2 points are sufficient to define a line, 3 points are sufficient to define a parabola, 4 points to define a cubic curve and so forth. That is, it takes $k$ points to define a polynomial of degree $k-1$.



'''

import random
from functools import reduce
from operator import add, mul
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.meta import field
from zkp_playground.algebra.utils import randfield


class SSSS:
    def __init__(self, F: FiniteField, secret=None, k=None, n=None, poly_params=None):
        self.F = F
        if all([secret, k, n]):
            self.setup(secret, k, n, poly_params)

    def setup(self, secret, k, n, poly_params=[]):
        '''
        k: threshold
        '''
        self.k = k
        self.n = n
        if not poly_params:
            poly_params = [randfield(self.F) for _ in range(k-1)]

        self.f = lambda x: self.F(secret) + reduce(
            add, [poly_params[i] * (x ** (i + 1)) for i in range(k-1)])

        return self

    def join(self, x=None):
        assert x != 0
        if not x:
            x = randfield(self.F)
        if not hasattr(self, 'f'):
            raise Exception("Needs to encrypt first")
        return (self.F(x), self.f(x))

    @staticmethod
    def decrypt(shares):
        x, fx = zip(*shares)
        k = len(fx)
        return reduce(add,
                      [fx[j] * reduce(
                          mul,
                          [x[m] / (x[m]-x[j]) for m in range(k-1) if m != j]) for j in range(k-1)])

    @classmethod
    def combine(cls, shares):
        return cls.decrypt(shares)
