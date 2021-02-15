from klefki.algebra.concrete import FiniteFieldCyclicSecp256k1 as CF


def test_int():
    x = CF(3)
    y = CF(4)
    assert x + y
    assert x - y
    assert x ** 2
    assert x * y
    assert x / y


def test_complex():
    x = CF(1+2j)
    y = CF(1+3j)

    assert x + y
    assert x * y
    assert (-x).__class__ == x.__class__
    assert x + (-y)
    assert x - y
