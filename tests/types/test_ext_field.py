from klefki.types.algebra.fields import PolyExtField
from klefki.curves.bn254 import FiniteFieldBN254 as F
modulus_coeffs = [82, 18]


class FQ2(PolyExtField):
    field = F
    modulus_coeffs = modulus_coeffs
    degree = len(modulus_coeffs)


def test_ext_field():
    x = FQ2([F(1), F(0)])
    f = FQ2([F(1), F(2)])
    fpx = FQ2([F(2), F(2)])
    one = FQ2.one()
    zero = FQ2.zero()

    assert x + f == fpx
    assert x - x == zero
