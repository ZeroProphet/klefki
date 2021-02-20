from klefki.curves.barreto_naehrig.bn128 import BN128ScalarFP as FP, ECGBN128 as ECG
from klefki.algebra.utils import randfield
from klefki.zkp import groth16
from klefki.zkp.r1cs import R1CS
from klefki.zkp.qap import QAP


@R1CS.r1cs(FP)
def f(x, k, c):
    y = x + c + k
    return y ** 3


g = ECG.G1
h = ECG.G2


def test_groth16():
    qap = QAP(f.A, f.B, f.C)
    U, V, W, T = qap.qap
    a = f.witness(FP(89), FP(8), FP(8))
    H = qap.H(a)
    R = groth16.RationalGenerator(
        FP, ECG, ECG, ECG, ECG.e, ECG.G1, ECG.G2, 4, U, V, W, T)
    tau, sigma = groth16.setup(R, len(a))
    pi = groth16.prov(R, H, tau, sigma, a)
    assert groth16.vfy(R, tau, a, pi)
