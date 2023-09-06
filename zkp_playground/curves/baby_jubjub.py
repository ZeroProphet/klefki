"""
DOC: https://eips.ethereum.org/EIPS/eip-2494
"""
import zkp_playground.const as const
from zkp_playground.algebra.fields import FiniteField
from zkp_playground.algebra.groups import EllipticCurveGroup
from zkp_playground.algebra.groups import EllipicCyclicSubgroup
from zkp_playground.curves.arith import short_weierstrass_form_curve_addition


class FiniteFieldBabyJubjub(FiniteField):
    P = const.BABYJUBJUB_P


class EllipticCurveBabyJubjub(EllipticCurveGroup):
    """
    Twisted Edwards Form (standard)
    y^2 = x^3 + Ax^2 + x
    Montgomery Form
    By^2 = x^3 + A x^2 + x
    """
    A = const.BABYJUBJUB_A
    B = const.BABYJUBJUB_B
    N = const.BABYJUBJUB_N

    def op(self, g):
        # x3 = (x1*y2 + y1*x2)/(1 + b*x1*x2*y1*y2)
        # y3 = (y1*y2 - a*x1*x2)/(1 - b*x1*x2*y1*y2)

        if g.value == 0:
            return self
        if self.value == 0:
            return g
        field = self.value[0].__class__

        m = field(self.B) * self.x * g.x * self.y * g.y

        x3 = (self.x * g.y + self.y * g.x) / (field(1) + m)
        y3 = (self.y * g.y - field(self.A) * self.x * g.x) / (field(1) - m)
        return self.__class__((x3, y3))


EllipticCurveBabyJubjub.G = EllipticCurveBabyJubjub((
    FiniteFieldBabyJubjub(const.BABYJUBJUB_Gx),
    FiniteFieldBabyJubjub(const.BABYJUBJUB_Gy)
))
