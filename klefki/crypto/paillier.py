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
        self.L  = lambda x: (x - 1) // self.N
        self.M = ~self.F(self.L(pow(self.G, self.Lam).value))


    @property
    def privkey(self):
        return (self.Lam, self.M)


    @property
    def pubkey(self):
        return (self.N, self.G)


    @classmethod
    def encrypt(cls, m, pub):
        N, G = pub

        if hasattr(m, "value"):
            m = m.value

        r = G.functor(random.randint(0, N))
        return G**m * r**N


    @classmethod
    def decrypt(cls, c, priv, pub):
        Lam, M = priv
        N, G = pub

        F = M.functor
        L =  lambda x: (x - 1) // N
        return F(L((c ** Lam).value)) * M

    def E(self, m, pub=None):
        return self.encrypt(m, pub or self.pubkey)


    def D(self, c, priv=None, pub=None):
        return self.decrypt(c, priv or self.privkey, pub or self.pubkey)


    def test(self):
        m = random.randint(0, self.N)
        assert m == self.D(self.E(m)).value
        return self
