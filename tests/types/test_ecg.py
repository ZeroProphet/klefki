from klefki.types.algebra.concrete import (
    EllipticCurveCyclicSubgroupSecp256k1 as CG,
)


N = CG.N
G = CG.G

def test_add():
    assert G - G == CG(0)
    assert G + G == G @ 2
