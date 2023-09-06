from zkp_playground.algebra.utils import randfield
from collections import namedtuple
from typing import Iterable, Tuple, Type
from operator import add
from functools import reduce

RationalGenerator = namedtuple("RelationGenerator", [
                               "F", "G1", "G2", "Gt", "e", "g", "h", "l", "U", "V", "W", "T"])


def setup(R: RationalGenerator, m: int) -> Tuple[Iterable, Tuple]:
    tau = alpha, beta, delta, gamma, x = \
        randfield(R.F), randfield(R.F), randfield(
            R.F), randfield(R.F), randfield(R.F)
    n = R.U[0].degree
    sigma_1 = [alpha, beta, delta] + \
              [x ** i for i in range(0, n)] + \
              [(R.U[i](x) * beta + R.V[i](x) * alpha + R.W[i](x)) / gamma for i in range(0, R.l)] + \
              [(R.U[i](x) * beta + R.V[i](x) * alpha + R.W[i](x)) / delta for i in range(R.l, m)] + \
              [(x ** i * R.T(x)) / delta for i in range(0, n-1)]
    sigma_2 = [beta, gamma, delta] + \
              [x**i for i in (0, n)]

    sigma = ([R.g @ s for s in sigma_1], [R.h @ s for s in sigma_2])
    return tau, sigma


def prov(R: RationalGenerator, H, tau, sigma, a) -> Tuple:
    r = randfield(R.F)
    s = randfield(R.F)
    alpha, beta, delta, gamma, x = tau
    m = len(a)
    A = alpha + reduce(add, [a[i] * (R.U[i](x))
                             for i in range(0, m)]) + r * delta
    B = beta + reduce(add, [a[i] * (R.V[i](x))
                            for i in range(0, m)]) + s * delta
    C = (reduce(add,
                [a[i]*(beta * (R.U[i](x)) + alpha * (R.V[i](x)) + R.W[i](x)) for i in range(R.l, m)])
         + H(x) * R.T(x)) / delta \
        + (A * s + B * r - r * s * delta)
    return (R.g @ A, R.g @ C, R.h @ B)


def vfy(R, tau, a, pi):
    alpha, beta, delta, gamma, x = tau
    A_1, C_1, B_2 = pi
    lhs = R.e(A_1, B_2)
    D = R.g @ (reduce(add, [
        a[i] * (beta * R.U[i](x) + alpha * R.V[i](x) + R.W[i](x))
        for i in range(0, R.l)]) / gamma)
    rhs = R.e(R.g @ alpha, R.h @ beta) * \
        R.e(D, R.h @ gamma) * \
        R.e(C_1, R.h @ delta)
    return lhs == rhs
