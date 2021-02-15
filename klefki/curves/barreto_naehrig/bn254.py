"""
ref: https://github.com/ethereum/research/blob/711bd9532b4534ef5ae6277bd7afe625195506d5/zksnark/bn128_field_elements.py
"""
import klefki.const as const
from klefki.algebra.fields import FiniteField
from klefki.algebra.groups import EllipticCurveGroup
from klefki.algebra.groups import EllipicCyclicSubgroup
from klefki.curves.arith import short_weierstrass_form_curve_addition2


class FiniteFieldBN254(FiniteField):
    P = const.BN254_P


class EllipticCurveBN254(EllipticCurveGroup):
    """
    Twisted Edwards Form (standard)
    y^2 = x^3 + Ax^2 + x
    Montgomery Form
    By^2 = x^3 + A x^2 + x
    """
    A = const.BN254_A
    B = const.BN254_B
    N = const.BN254_N

    def op(self, g):
        if g == self.zero():
            return self
        if self == self.zero():
            return g
        field = self.id[0].type

        # a1,a3,a2,a4,a6 = 0, 0, 0, a, b
        x, y = short_weierstrass_form_curve_addition2(
            self.x, self.y,
            g.x, g.y,
            field(0),
            field(0),
            field(0),
            field(self.A),
            field(self.B),
            field
        )
        if x == y == field(0):
            return self.__class__(0)
        return self.__class__((x, y))


EllipticCurveBN254.G = EllipticCurveBN254((
    FiniteFieldBN254(const.BN254_Gx),
    FiniteFieldBN254(const.BN254_Gy)
))
