# ref: https://blog.decentriq.ch/zk-snarks-primer-part-one/

from typing import Iterable
from typing import Type
from klefki.algebra.fields import FiniteField
from klefki.algebra.rings import PolyRing
from klefki.zkp.r1cs import R1CS, mul as vmul
from functools import partial, reduce
from operator import add, mul

__all__ = ["QAP"]


def vec2polyring(m):
    return [PolyRing.lagrange_interp(x) for x in map(list, zip(*m))]


class QAP:
    def __init__(self,
                 A=Iterable,
                 B=Iterable,
                 C=Iterable):
        field = A[0][0].type
        self.Z = lambda x: reduce(mul, [(x - field(i))
                                        for i in range(1, len(A)+1)])
        (self.A, self.B, self.C) = (vec2polyring(i) for i in [A, B, C])

    @property
    def qap(self):
        return (self.A, self.B, self.C)

    def proof(self, c: FiniteField, s: Iterable[FiniteField]):
        """
        c: Callange
        s: witness vertex
        """
        A = sum(vmul([f(c) for f in self.A], s))
        B = sum(vmul([f(c) for f in self.B], s))
        C = sum(vmul([f(c) for f in self.C], s))
        Z = self.Z(c)
        H = (A * B - C) * (Z ** (-1))
        return (A, B, C, Z, H)

    def verify(s, A, B, C, Z, H):
        return A * B - C == H * Z
