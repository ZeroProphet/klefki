from klefki.algebra.concrete import (
    EllipticCurveGroupSecp256k1 as CG,
    FiniteFieldCyclicSecp256k1 as CF
)


N = CG.N
G = CG.G


def test_add():
    assert G - G == CG(0)
    assert G + G == G @ CF(2)
