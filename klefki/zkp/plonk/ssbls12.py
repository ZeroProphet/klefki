from klefki.curves.bls12_381 import BLS12_381ScalarHashableFP as Fp
from klefki.curves.bls12_381 import ECGBLS12_381 as ECG

from .polynomial import polynomialsOver

Poly = polynomialsOver(Fp)


class SS_BLS12_381:
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    # def in_group(self):
    #     return bls12_381.pairing(self.m2, bls12_381.G1) == bls12_381.pairing(
    #         bls12_381.G2, self.m1
    #     )

    # order = bls12_381.curve_order

    def __add__(self, other):
        assert type(other) is SS_BLS12_381
        return SS_BLS12_381(self.m1 + other.m1, self.m2 + other.m2)

    def __mul__(self, x):
        assert type(x) in (int, Fp)
        # TODO: i think in klefki we can use x.value
        # if type(x) is Fp:
        #     x = x.n
        return SS_BLS12_381(self.m1 @ x, self.m2 @ x)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __eq__(self, other):
        return self.m1 == other.m1 and self.m2 == other.m2

    def pair(self, other):
        t1 = ECG.pairing(other.m1, self.m2)
        # t2 = bls12_381.pairing(other.m2, self.m1)
        # assert t1 == t2
        return t1

    def __repr__(self):
        return repr(self.m1)


SS_BLS12_381.G = SS_BLS12_381(ECG.G1, ECG.G2)
SS_BLS12_381.GT = SS_BLS12_381.G.pair(SS_BLS12_381.G)
Group = SS_BLS12_381