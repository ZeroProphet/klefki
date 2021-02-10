from klefki.types.algebra.fields import PolyExtField
from klefki.curves.barreto_naehrig.bn128 import BN128FP as F


modulus_coeffs = [82, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0]


class FQ12(PolyExtField):
    F = F
    E = modulus_coeffs


def test_ext_field():
    x = FQ12([1] + [0] * 11)
    f = FQ12([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    fpx = FQ12([2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    one = FQ12.one()
    zero = FQ12.zero()

    assert x + f == fpx
    assert x - x == zero
    assert f - f == zero
    assert x * x == one
    assert x / x == one
    assert f / f == one
    assert f / f == one
    assert one / f + x / f == (one + x) / f
    assert one * f + x * f == (one + x) * f
    assert x ** (F.P - 1) == one
