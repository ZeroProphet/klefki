"""
Ref: https://byt3bit.github.io/primesym/mimc/
Ref: https://eprint.iacr.org/2016/492.pdf
"""

from zkp_playground.curves.baby_jubjub import FiniteFieldBabyJubjub as F
from zkp_playground.algebra.utils import randfield
from zkp_playground.utils import to_sha256int
from zkp_playground.zkp.r1cs import R1CS
from functools import partial, reduce
from itertools import count
import time
from hashlib import sha256


class MiMC:
    @staticmethod
    def F(x, k, c):
        return (x + k + c) ** 3

    def __init__(self, field, r):
        self.field = field
        self.c = [field(0)] + [randfield(field) for i in range(1, r)]
        self.r = r

    def encrypt(self, x, k, r=None):
        if not r:
            r = self.r
        return self.r1cs(x, k)

    @property
    def r1cs(self):
        r = self.r
        c = self.c

        @R1CS.r1cs(self.field, self.__dict__)
        def mimc(x, k):
            for i in range(r):
                # x + k + c_i
                x = x + k
                x = x + c[i]
                # x ^ 3
                x = x ** 3
            return x + k
        return mimc

    def E(self, *args, **kwargs):
        return self.encrypt(*args, **kwargs)

    @property
    def constants(self):
        return self.c


class FeistelMiMC(MiMC):

    @staticmethod
    def F(x, y, k, c):
        return (y, x + (y + k + c) ** 3)

    def encrypt(self, x, y, k, r=None):
        if not r:
            r = self.r
        Ks = [(i + self.field(1)) * k for i in range(0, r)]
        Fs = [partial(self.F, k=k, c=c) for (k, c) in zip(Ks[:r], self.c[:r])]
        return reduce(
            lambda x, y: y(*x), Fs[1:], Fs[0](x, y)
        ) + (k, k)

    @property
    def r1cs(self):
        r = self.r
        c = self.c

        @R1CS.r1cs(self.field, self.__dict__)
        def mimc(x, y, k):
            for i in range(r):
                # k = k * (i+1)
                j = i + 1
                # (y, x) = (x, x + (y+k+c) ** 3)
                m = y + k * j + c[i]
                m = m ** 3 + m
                m = x + m
                x = y
                y = m
            return x + y
        return mimc
