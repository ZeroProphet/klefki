# ref: https://blog.decentriq.ch/zk-snarks-primer-part-one/

from typing import Iterable
from typing import Type
from klefki.algebra.fields import FiniteField
from klefki.zkp.r1cs import R1CS, mul as vmul
from functools import partial, reduce
from operator import add, mul


def lagrange_polynomial(xs, ys, field=int):
    k = len(xs)

    def l(j): return lambda x: reduce(
        mul, [(x-xs[m])/(xs[j]-xs[m]) for m in range(0, k) if m != j])

    return lambda x: field(reduce(add, [ys[j] * l(j)(x) for j in range(0, k)]))


def transfer(v, field=int):
    ret = []
    for n in range(len(v[0])):
        a = []
        for i in range(len(v)):
            a.append(field(v[i][n]))
        ret.append(
            lagrange_polynomial(
                [field(i) for i in range(1, len(a)+1)],
                a,
                field
            )
        )
    return lambda x: [f(x) for f in ret]


def map2field(v, field=int):
    return [[field(j) for j in i] for i in v]


def R1CS2QAP(a, b, c, x=None, field=int):
    #    s = [field(i) for i in s]
    a = map2field(a, field)
    b = map2field(b, field)
    c = map2field(c, field)
    A = transfer(a, field)
    B = transfer(b, field)
    C = transfer(c, field)

    def Z(x):
        return reduce(mul, [(x - field(i)) for i in range(1, len(a)+1)])
    if not x:
        return A, B, C, Z
    return (A(x), B(x), C(x), Z(x))


class QAP:
    def __init__(self, F: Type[FiniteField], A=Iterable[F], B=Iterable[F], C=Iterable[F]):
        (self.A, self.B, self.C, self.Z) = R1CS2QAP(A, B, C, field=F)

    def proof(self, c: Field, s: Iterable[FiniteField]):
        """
        c: Callange
        s: witness vertex
        """
        A = sum(vmul(self.A(st), s))
        B = sum(vmul(self.B(st), s))
        C = sum(vmul(self.C(st), s))
        Z = self.Z(st)
        H = (A * B - C) * (Z ** (-1))
        return (A, B, C, Z, H)

    def verify(s, A, B, C, Z, H):
        return A * B - C == H * Z
