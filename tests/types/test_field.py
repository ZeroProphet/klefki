from klefki.types.algebra.concrete import FiniteFieldCyclicSecp256k1 as CF

def test_complex():
    x = CF(1+2j)
    y = CF(1+3j)

    assert x + y
    assert x * y
