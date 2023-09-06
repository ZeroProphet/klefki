from functools import partial
from zkp_playground.zkp.groth16.r1cs import R1CS, mul
from zkp_playground.zkp.groth16.qap import QAP
from zkp_playground.curves.bns.bn128 import BN128FP as F
from zkp_playground.algebra.rings import PolyRing

# map int to field
ciphers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
times = 5


@R1CS.r1cs(F)
def f(x, k, c):
    y = x + c + k
    return y ** 3


@R1CS.r1cs(F, globals())
def mimc(x, k):
    for i in range(times):
        c = ciphers[i]
        x = f(x, k, c)
    return x + k


def test_qap():
    A, B, C = mimc.r1cs
    qap = QAP(A, B, C)
    w = mimc.witness(F(42))
    c = F(1231314145125)
    assert qap.verify(*qap.proof(F(112221), w))
