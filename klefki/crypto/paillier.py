from math import gcd
from abc import ABCMeta, abstractproperty
from random import randint
from klefki.types.algebra.utils import randfield
from klefki.types.algebra.meta import field
from klefki.numbers import lcm
import random


class Paillier(metaclass=ABCMeta):

    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
        assert gcd(P * Q, (P - 1) * (Q - 1)) == 1

        self.N = P * Q
        self.Lam = lcm(P - 1, Q - 1)

        self.F = field(self.N)
        self.DF = field(self.N**2)

        self.G = randfield(self.DF)
        self.L = L = lambda x: (x - 1) // self.N
        self.M = ~self.F(self.L(pow(self.G, self.Lam).value))


    @property
    def privkey(self):
        return (self.Lam, self.M)


    @property
    def pubkey(self):
        return (self.N, self.G)


    def encrypt(self, m):
        if hasattr(m, "value"):
            m = m.value
        assert 0 <= m < self.N
        r = self.DF(random.randint(0, self.N))
        return self.G**m * r**self.N


    def decrypt(self, c):
        return self.F(self.L((c ** self.Lam).value)) * self.M

    def E(self, m):
        return self.encrypt(m)


    def D(self, m):
        return self.decrypt(m)


    def test(self):
        m = random.randint(0, self.N)
        assert m == self.D(self.E(m)).value
        return self
