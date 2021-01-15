"""
Ref: https://byt3bit.github.io/primesym/mimc/
Ref: https://eprint.iacr.org/2016/492.pdf
"""

from klefki.curves.baby_jubjub import FiniteFieldBabyJubjub as F
from klefki.types.algebra.utils import randfield
from klefki.utils import to_sha256int
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
        if not r: r = self.r
        Fs = [partial(self.F, k=k, c=c) for c in self.c[:r]]
        return reduce(lambda x, y: x + y(x), Fs[1:], Fs[0](x)) + k

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
        if not r: r = self.r
        Ks = [(i + self.field(1)) * k for i in range(0, r)]
        Fs = [partial(self.F, k=k, c=c) for (k, c) in zip(Ks[:r], self.c[:r])]
        return reduce(
            lambda x, y: y(*x), Fs[1:], Fs[0](x, y)
        ) + (k, k)
