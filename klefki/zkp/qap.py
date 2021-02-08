# ref: https://blog.decentriq.ch/zk-snarks-primer-part-one/

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
            a.append(v[i][n])
        ret.append(lagrange_polynomial([field(i)
                                        for i in range(1, len(a)+1)], a, field))
    return lambda x: [f(x) for f in ret]


def map2field(v, field=int):
    return [[field(j) for j in i]for i in v]


def R1CS2QAP(a, b, c, x=None, field=int):
    #    s = [field(i) for i in s]
    a = map2field(a, field)
    b = map2field(b, field)
    c = map2field(c, field)
    A = transfer(a, field)
    B = transfer(b, field)
    C = transfer(c, field)

    def Z(x): return reduce(mul, [(x - field(i)) for i in range(1, len(a)+1)])
    if not x:
        return A, B, C, Z
    return (A(x), B(x), C(x), Z(x))


def proof(s, A, B, C, Z, field=int):
    s = [field(i) for i in s]
    A = sum(vmul(A, s))
    B = sum(vmul(B, s))
    C = sum(vmul(C, s))
    H = (A * B - C) * (Z ** (-1))
    assert A * B - C == H * Z
    return (s, H)


def verify(s, A, B, C, Z, H):
    return sum(vmul(A, s)) * sum(vmul(B, s)) - sum(vmul(C, s)) == H * Z
