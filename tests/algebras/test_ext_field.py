from klefki.algebra.fields import PolyExtField
from klefki.curves.barreto_naehrig.bn128 import BN128FP as FQ
from klefki.curves.barreto_naehrig.bn128 import BN128FP2 as FQ2


modulus_coeffs = [82, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0]


class FQ12(PolyExtField):
    F = FQ
    E = modulus_coeffs


def test_field():
    assert FQ(2) * FQ(2) == FQ(4)
    assert FQ(2) / FQ(7) + FQ(9) / FQ(7) == FQ(11) / FQ(7)
    assert FQ(2) * FQ(7) + FQ(9) * FQ(7) == FQ(11) * FQ(7)
    assert FQ(9) ** FQ.P == FQ(9)


def test_fq2():
    x = FQ2([1, 0])
    f = FQ2([1, 2])
    fpx = FQ2([2, 2])
    one = FQ2.one()

    # Check that the field works fine
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (FQ.P ** 2 - 1) == one


def test_fq12():
    x = FQ12([1] + [0] * 11)
    f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    one = FQ12.one()
    assert x == one
    # Check that the field works fine
    assert x + f == fpx
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (FQ.P ** 12 - 1) == one
