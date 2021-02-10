"""
ref: https://github.com/ethereum/research/blob/711bd9532b4534ef5ae6277bd7afe625195506d5/zksnark/bn128_field_elements.py
"""
import klefki.const as const
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.fields import PolyExtField
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.groups import EllipicCyclicSubgroup
from klefki.curves.arith import short_weierstrass_form_curve_addition2


class BN128FP(FiniteField):
    P = const.BN128_P


class BN128FP2(PolyExtField):
    F = BN128FP
    E = const.BN128_FP2_E


class BN128FP12(PolyExtField):
    F = BN128FP
    E = const.BN128_FP12_E


class EllipticCurveBN128(EllipticCurveGroup):
    A = const.BN128_A
    B = const.BN128_B

    def op(self, g):
        if g.id == self.zero():
            return self
        if self.value == self.zero():
            return g
        field = self.id[0].functor

        # a1,a3,a2,a4,a6 = 0, 0, 0, a, b
        x, y = short_weierstrass_form_curve_addition2(
            self.x, self.y,
            g.x, g.y,
            field.zero(),
            field.zero(),
            field.zero(),
            field(self.A),
            field(self.B),
            field
        )
        if x == y == field.zero():
            return self.zero()
        return self.__class__((x, y))
