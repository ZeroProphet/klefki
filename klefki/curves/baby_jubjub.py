"""
DOC: https://eips.ethereum.org/EIPS/eip-2494

"""

import klefki.const as const
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.groups import EllipicCyclicSubgroup


class FiniteFieldBabyJubjub(FiniteField):
    P = const.BABYJUBJUB_P


class EllipticCurveBabyJubjub(EllipticCurveGroup):
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
