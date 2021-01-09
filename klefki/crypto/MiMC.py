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
