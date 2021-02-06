"""
DOC: https://eips.ethereum.org/EIPS/eip-2494
"""
import klefki.const as const
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.groups import EllipicCyclicSubgroup
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
        if g.value == 0:
            return self
        if self.value == 0:
            return g
        field = self.value[0].__class__

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
    FiniteFieldBN254(const.BN254_B)
))
