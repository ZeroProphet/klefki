# ref: https://blog.decentriq.ch/zk-snarks-primer-part-one/

from klefki.zkp.r1cs import R1CS, mul as vmul
from functools import partial, reduce
from operator import add, mul


def lagrange_polynomial(xs, ys, field=int):
    k = len(xs)
    l = lambda j: lambda x: reduce(mul, [(x-xs[m])/(xs[j]-xs[m]) for m in range(0, k) if m != j])
    return lambda x: field(reduce(add, [ys[j] * l(j)(x) for j in range(0, k)]))


def transfer(v, field=int):
    ret = []
    for n in range(len(v[0])):
        a = []
        for i in range(len(v)):
            a.append(v[i][n])
        ret.append(lagrange_polynomial([field(i) for i in range(1, len(a)+1)], a, field))
    return lambda x: [f(x) for f in ret]


def map2field(v, field=int):
    return [[field(j) for j in i]for i in v]


def R1CS2QAP(s, A, B, C, field=int):
    s = [field(i) for i in s]
    A = map2field(A, field)
    B = map2field(B, field)
    C = map2field(C, field)
    A_v = transfer(A, field)
    B_v = transfer(B, field)
    C_v = transfer(C, field)
    A = lambda x: sum(vmul(A_v(x), s))
    B = lambda x: sum(vmul(B_v(x), s))
    C = lambda x: sum(vmul(C_v(x), s))
    Z = lambda x: field((x-field(1)) * (x-field(2)))
    H = lambda x: field((A(x) * B(x) - C(x)) * (Z(x) ** -1))
    return (A, B, C, Z, H)


def verify_qap(A, b, C, Z, H):
    return A(x) * B(x) - C(x) == H(x) * Z(x)
