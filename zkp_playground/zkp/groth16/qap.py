# ref: https://blog.decentriq.ch/zk-snarks-primer-part-one/

from typing import Iterable
from typing import Type
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.rings import PolyRing
from zkp_playground.algebra.utils import randfield
from zkp_playground.zkp.groth16.r1cs import R1CS, mul as vmul
from functools import partial, reduce
from itertools import starmap
from operator import add, mul

__all__ = ["QAP"]


def vec2polyring(m):
    return [PolyRing.lagrange_interp(x) for x in map(list, zip(*m))]


class QAP:
    """
    Given $n$ equations we pick arbitrary distinct $r_1,\cdots,r_n \in \mathbb{F}$ and define
    $$
    t(x) = \prod_{q=1}^n (x - r_q)
    $$
    Since $t(X)$ is the lowest degreee monomial with $t(r_q) = 0 $ in each point, we can refomulate as:
    $$
    \sum_{i=0}^m a_i u_i(X) \circ \sum_{i=0}^m a_i v_i(X) = \sum_{i=0}^m a_i w_i(X) \mod t(X)
    $$
    we will be working with quadratic arithmetic programsRthat have thefollowing description

    $$
    R = (\mathbb{F}, aux, l, \{u_i(X), v_i(X), w_i(X)\}_{i=0}^n, t(X))
    $$
    """

    def __init__(self,
                 A=Iterable,
                 B=Iterable,
                 C=Iterable):
        # t(x) = \prod_{q=1}^n (x - r_q)

        self.field = A[0][0].type
        # self.Z = lambda x: reduce(mul,
        #                      [(x - randfield(field))
        #                       for i in range(1, len(A)+1)])
        (self.A, self.B, self.C) = (vec2polyring(i) for i in [A, B, C])

        Z = PolyRing([self.field.one()])
        for i in range(1, self.A[0].degree - 1):
            Z = Z * PolyRing(-randfield(self.field), self.field.one())
        self.Z = Z

    def O(self, ws):
        A = PolyRing.zero()
        for w, a in zip(ws, self.A):
            A = A + PolyRing([w]) * a

        B = PolyRing.zero()
        for w, b in zip(ws, self.B):
            B = B + PolyRing([w]) * b

        C = PolyRing.zero()
        for w, c in zip(ws, self.C):
            C = C + PolyRing([w]) * c

        O = A * B - C
        return O

    def H(self, ws):
        return lambda x: self.O(ws)(x) / self.Z(x)

    @property
    def qap(self):
        return (self.A, self.B, self.C, self.Z)

    def proof(self, x: FiniteField, s: Iterable[FiniteField], start=0, end=None):
        """
        c: Callange
        s: witness vertex
        """
        end = end or len(s)
        A = reduce(add, starmap(
            mul, zip(s[start:end], map(lambda a: a(x), self.A[start:end]))))
        B = reduce(add, starmap(
            mul, zip(s[start:end], map(lambda b: b(x), self.B[start:end]))))
        C = reduce(add, starmap(
            mul, zip(s[start:end], map(lambda c: c(x), self.C[start:end]))))
        Z = self.Z(x)
        H = self.H(s)(x)
        return (A, B, C, Z, H)

    def verify(s, A, B, C, Z, H):
        return A * B == H * Z + C
